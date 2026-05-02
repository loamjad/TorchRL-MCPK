import numpy as np
from src.sim.util.axis_aligned_bb import AxisAlignedBB

class Entity:
    def __init__(self):
        self.width = np.float32(0.6)
        self.height = np.float32(1.8)

        self.set_position(np.float64(0.0), np.float64(0.0), np.float64(0.0))

        self.pos_x = np.float64(0.0)
        self.pos_y = np.float64(0.0)
        self.pos_z = np.float64(0.0)
        self.motion_x = np.float64(0.0)
        self.motion_y = np.float64(0.0)
        self.motion_z = np.float64(0.0)
        self.rotation_yaw = np.float32(0.0)
        self.rotation_pitch = np.float32(0.0)
        self.on_ground = False
        self.is_collided_horizontally = False
        self.is_collieded_vertically = False
        self.is_collided = False

        self.last_tick_pos_x = np.float64(0.0)
        self.last_tick_pos_y = np.float64(0.0)
        self.last_tick_pos_z = np.float64(0.0)
        self.is_air_borne = False

    def set_position(x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z
        f = self.width/np.float32(2.0)
        f1 = self.height
        self.set_entity_bounding_box(
            AxisAlignedBB(
                x - np.float64(f),
                y,
                z - np.float64(f),
                x + np.float64(f),
                y + np.float64(f1),
                z + np.float64(f)
            )
        )

    def set_entity_bounding_box():
        pass

    def get_jump_upwards_motion(self):
        return 0.42

    def jump(self):
        self.motiony = self.get_jump_upwards_motion()
        self.is_airborne = True

    def move_entity_with_heading(self, strafe, forward):
        self.motiony -= 0.08
        self.motiony *= 0.98

    def on_living_update(self):
        if self.jump_ticks > 0:
            self.jump_ticks -= 1

        if abs(self.motiony) < 0.005:
            self.motiony = 0.0

        if self.input.get_jump():
            if self.on_ground and self.jump_ticks == 0:
                self.jump()
                self.jump_ticks = 10
        else:
            self.jump_ticks = 0

        move_forward = (1.0 if self.input.get_forward() else 0.0) - (1.0 if self.input.get_backward() else 0.0)
        move_strafe = (1.0 if self.input.get_left() else 0.0) - (1.0 if self.input.get_right() else 0.0)
        self.move_entity_with_heading(move_strafe, move_forward)
