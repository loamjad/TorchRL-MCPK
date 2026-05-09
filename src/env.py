from collections import deque

import numpy as np
import torch
from tensordict import TensorDict
from torchrl.data import Bounded, Composite, Unbounded
from torchrl.envs import EnvBase

from src.sim.entity.player.entity_player_mp import EntityPlayerMP


class Course:
    """Parkour course data used by the TorchRL env.

    This is intentionally small for now. The env depends on this interface so the
    simulator can later replace the rough grid pathing with Minecraft-accurate
    collision, jump arcs, checkpoints, ladders, slime, water, and other mechanics.
    """

    def __init__(self, blocks=(), bounds=None, margin=8):
        self.blocks = {self._as_cell(block) for block in blocks}
        self.bounds = bounds
        self.margin = int(margin)

    def distance_to_finish(self, start_position, finish_position):
        # TODO(sim): Replace this simple voxel BFS with a movement-aware parkour
        # planner once the simulator understands real block collision and jumps.
        start = self.position_to_cell(start_position)
        finish = self.position_to_cell(finish_position)
        if self.is_blocked(start) or self.is_blocked(finish):
            return None

        bounds = self._bounds_for(start, finish)
        queue = deque([(start, 0)])
        visited = {start}

        while queue:
            cell, distance = queue.popleft()
            if cell == finish:
                return float(distance)

            for neighbor in self._neighbors(cell):
                if neighbor in visited:
                    continue
                if not self._in_bounds(neighbor, bounds):
                    continue
                if self.is_blocked(neighbor):
                    continue
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

        return None

    def is_blocked(self, cell):
        return self._as_cell(cell) in self.blocks

    def position_to_cell(self, position):
        return self._as_cell(np.floor(position).astype(np.int64))

    def _bounds_for(self, start, finish):
        if self.bounds is not None:
            return tuple((int(low), int(high)) for low, high in self.bounds)

        cells = list(self.blocks) + [start, finish]
        mins = [min(cell[axis] for cell in cells) - self.margin for axis in range(3)]
        maxs = [max(cell[axis] for cell in cells) + self.margin for axis in range(3)]
        mins[1] = min(cell[1] for cell in cells)
        return tuple(zip(mins, maxs))

    @staticmethod
    def _neighbors(cell):
        x, y, z = cell
        return (
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        )

    @staticmethod
    def _in_bounds(cell, bounds):
        return all(low <= value <= high for value, (low, high) in zip(cell, bounds))

    @staticmethod
    def _as_cell(cell):
        x, y, z = cell
        return (int(x), int(y), int(z))


class PlayerInput:
    def __init__(self):
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.jump = False

    def set_from_action(self, action):
        self.forward = bool(action[0] > 0.5)
        self.backward = bool(action[1] > 0.5)
        self.left = bool(action[2] > 0.5)
        self.right = bool(action[3] > 0.5)
        self.jump = bool(action[4] > 0.5)

    def get_forward(self):
        return self.forward

    def get_backward(self):
        return self.backward

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_jump(self):
        return self.jump


class MinecraftTorchRLEnv(EnvBase):
    """A tick-based Minecraft-style player movement environment for TorchRL.

    The sim advances one Minecraft tick per step at 20 ticks per second. Actions
    are a seven-value tensor:

    0. forward button
    1. backward button
    2. left strafe button
    3. right strafe button
    4. jump button
    5. yaw delta, scaled by ``max_yaw_delta``
    6. pitch delta, scaled by ``max_pitch_delta``
    """

    metadata = {"render_modes": []}

    def __init__(
        self,
        *,
        device=None,
        max_ticks=None,
        start_position=(0.0, 0.0, 0.0),
        finish_position=(0.0, 0.0, 10.0),
        finish_radius=0.6,
        course=None,
        course_blocks=(),
        course_bounds=None,
        unreachable_distance=1000.0,
        tick_rate=20,
        max_yaw_delta=10.0,
        max_pitch_delta=10.0,
        goal_reward=100.0,
        time_penalty=0.01,
    ):
        super().__init__(device=device, batch_size=[])
        self.tick_rate = int(tick_rate)
        self.dt = 1.0 / float(self.tick_rate)
        self.max_ticks = max_ticks
        self.start_position = np.asarray(start_position, dtype=np.float64)
        self.finish_position = np.asarray(finish_position, dtype=np.float64)
        self.finish_radius = float(finish_radius)
        if course is None:
            course = Course(blocks=course_blocks, bounds=course_bounds)
        self.course = course
        self.unreachable_distance = float(unreachable_distance)
        self.max_yaw_delta = float(max_yaw_delta)
        self.max_pitch_delta = float(max_pitch_delta)
        self.goal_reward = float(goal_reward)
        self.time_penalty = float(time_penalty)
        self.rng = torch.Generator(device=self.device)
        self.player = None
        self.tick_count = 0
        self.previous_distance_to_finish = 0.0
        self._make_specs()

    def _make_specs(self):
        self.observation_spec = Composite(
            observation=Unbounded(shape=(18,), dtype=torch.float32, device=self.device),
            position=Unbounded(shape=(3,), dtype=torch.float32, device=self.device),
            finish_position=Unbounded(shape=(3,), dtype=torch.float32, device=self.device),
            distance_to_finish=Unbounded(shape=(1,), dtype=torch.float32, device=self.device),
            motion=Unbounded(shape=(3,), dtype=torch.float32, device=self.device),
            rotation=Bounded(
                low=torch.tensor([-180.0, -90.0], device=self.device),
                high=torch.tensor([180.0, 90.0], device=self.device),
                shape=(2,),
                dtype=torch.float32,
                device=self.device,
            ),
            on_ground=Unbounded(shape=(1,), dtype=torch.bool, device=self.device),
            tick=Unbounded(shape=(1,), dtype=torch.int64, device=self.device),
            shape=(),
            device=self.device,
        )
        self.action_spec = Bounded(
            low=-1.0,
            high=1.0,
            shape=(7,),
            dtype=torch.float32,
            device=self.device,
        )
        self.reward_spec = Unbounded(shape=(1,), dtype=torch.float32, device=self.device)

    def _set_seed(self, seed):
        self.rng = torch.Generator(device=self.device)
        if seed is None:
            seed = torch.seed()
        self.rng.manual_seed(seed)

    def _reset(self, tensordict=None, **kwargs):
        self.player = EntityPlayerMP()
        self.player.input = PlayerInput()
        self.player.on_ground = True
        self.player.set_position(*self.start_position)
        self.tick_count = 0
        self.previous_distance_to_finish = self._distance_to_finish()
        return self._make_tensordict()

    def _step(self, tensordict):
        if self.player is None:
            self._reset()

        action = tensordict.get("action").detach().to("cpu").float().numpy()
        self.player.input.set_from_action(action)
        self._apply_look(action[5], action[6])
        self.player.on_update()
        self.tick_count += 1

        reward = self._reward()
        self.previous_distance_to_finish = self._distance_to_finish()
        out = self._make_tensordict()
        out.set("reward", reward)
        done = self._done()
        out.set("done", done)
        out.set("terminated", self._success())
        return out

    def _apply_look(self, yaw_action, pitch_action):
        self.player.rotation_yaw = np.float32(
            self._wrap_degrees(
                self.player.rotation_yaw + (float(yaw_action) * self.max_yaw_delta)
            )
        )
        self.player.rotation_pitch = np.float32(
            np.clip(
                self.player.rotation_pitch
                + (float(pitch_action) * self.max_pitch_delta),
                -90.0,
                90.0,
            )
        )

    def _make_tensordict(self):
        position = torch.tensor(
            [self.player.pos_x, self.player.pos_y, self.player.pos_z],
            dtype=torch.float32,
            device=self.device,
        )
        finish_position = torch.tensor(
            self.finish_position,
            dtype=torch.float32,
            device=self.device,
        )
        distance_to_finish = torch.tensor(
            [self._distance_to_finish()],
            dtype=torch.float32,
            device=self.device,
        )
        motion = torch.tensor(
            [self.player.motion_x, self.player.motion_y, self.player.motion_z],
            dtype=torch.float32,
            device=self.device,
        )
        rotation = torch.tensor(
            [self.player.rotation_yaw, self.player.rotation_pitch],
            dtype=torch.float32,
            device=self.device,
        )
        on_ground = torch.tensor(
            [self.player.on_ground], dtype=torch.bool, device=self.device
        )
        tick = torch.tensor([self.tick_count], dtype=torch.int64, device=self.device)
        observation = torch.cat(
            (
                position,
                finish_position,
                distance_to_finish,
                motion,
                rotation,
                on_ground.to(torch.float32),
                tick.to(torch.float32),
                torch.tensor(
                    [
                        self.player.last_tick_pos_x,
                        self.player.last_tick_pos_y,
                        self.player.last_tick_pos_z,
                        self.dt,
                    ],
                    dtype=torch.float32,
                    device=self.device,
                ),
            )
        )
        return TensorDict(
            {
                "observation": observation,
                "position": position,
                "finish_position": finish_position,
                "distance_to_finish": distance_to_finish,
                "motion": motion,
                "rotation": rotation,
                "on_ground": on_ground,
                "tick": tick,
            },
            batch_size=[],
            device=self.device,
        )

    def _reward(self):
        distance = self._distance_to_finish()
        progress = self.previous_distance_to_finish - distance
        reward = progress - self.time_penalty
        if self._is_success_distance(distance):
            reward += self.goal_reward
        return torch.tensor([reward], dtype=torch.float32, device=self.device)

    def _done(self):
        done = self._success().item()
        if self.max_ticks is not None:
            done = done or self.tick_count >= self.max_ticks
        return torch.tensor([done], dtype=torch.bool, device=self.device)

    def _success(self):
        return torch.tensor(
            [self._is_success_distance(self._distance_to_finish())],
            dtype=torch.bool,
            device=self.device,
        )

    def _distance_to_finish(self):
        position = np.asarray(
            [self.player.pos_x, self.player.pos_y, self.player.pos_z],
            dtype=np.float64,
        )
        distance = self.course.distance_to_finish(position, self.finish_position)
        if distance is None:
            return self.unreachable_distance
        return distance

    def _is_success_distance(self, distance):
        return distance <= self.finish_radius

    @staticmethod
    def _wrap_degrees(value):
        return ((value + 180.0) % 360.0) - 180.0


__all__ = ["Course", "MinecraftTorchRLEnv", "PlayerInput"]
