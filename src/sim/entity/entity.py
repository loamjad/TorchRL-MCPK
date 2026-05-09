import numpy as np
from src.sim.util.axis_aligned_bb import AxisAlignedBB


class Entity:
    def __init__(self):
        self.width = np.float32(0.6)
        self.height = np.float32(1.8)

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
        self.is_collided_vertically = False
        self.is_collided = False

        self.last_tick_pos_x = np.float64(0.0)
        self.last_tick_pos_y = np.float64(0.0)
        self.last_tick_pos_z = np.float64(0.0)
        self.is_air_borne = False
        self.bounding_box = None
        self.set_position(np.float64(0.0), np.float64(0.0), np.float64(0.0))

<<<<<<< HEAD
        self.bounding_box = None
        self.prev_pos_x = np.float64(0.0)
        self.prev_pos_y = np.float64(0.0)
        self.prev_pos_z = np.float64(0.0)
        self.prev_rotation_yaw = np.float32(0.0)
        self.prev_rotation_pitch = np.float32(0.0)
        self.distance_walked_modified = np.float32(0.0)
        self.prev_distance_walked_modified = np.float32(0.0)

=======
>>>>>>> 01f7beb6a21a8ae274b00b55083c90b9336c2487
    def set_position(self, x, y, z):
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

<<<<<<< HEAD
    def set_entity_bounding_box(self, bb: AxisAlignedBB):
        self.bounding_box = bb
=======
    def set_entity_bounding_box(self, bounding_box):
        self.bounding_box = bounding_box
>>>>>>> 01f7beb6a21a8ae274b00b55083c90b9336c2487

    def get_jump_upwards_motion(self):
        return 0.42

    def jump(self):
        self.motion_y = self.get_jump_upwards_motion()
        self.is_air_borne = True

    def move_entity(self, x, y, z):
        # TODO(sim): Resolve motion against Course collision instead of only using
        # a flat floor. The TorchRL env already routes reward through Course.
        self.is_collided_horizontally = False
        self.is_collided_vertically = False

        next_y = self.pos_y + y
        if next_y <= 0.0:
            y = -self.pos_y
            self.motion_y = np.float64(0.0)
            self.on_ground = True
            self.is_collided_vertically = True
        else:
            self.on_ground = False

        self.set_position(self.pos_x + x, self.pos_y + y, self.pos_z + z)
        self.is_collided = (
            self.is_collided_horizontally or self.is_collided_vertically
        )

    def move_flying(self, strafe, forward, friction):
        strafe = np.float64(strafe)
        forward = np.float64(forward)
        speed = strafe * strafe + forward * forward
        if speed < 1.0e-4:
            return

        speed = np.sqrt(speed)
        if speed < 1.0:
            speed = 1.0
        scale = np.float64(friction) / speed
        strafe *= scale
        forward *= scale

        yaw = np.deg2rad(self.rotation_yaw)
        sin_yaw = np.sin(yaw)
        cos_yaw = np.cos(yaw)
        self.motion_x += strafe * cos_yaw - forward * sin_yaw
        self.motion_z += forward * cos_yaw + strafe * sin_yaw

    def move_entity_with_heading(self, strafe, forward):
        if self.on_ground:
            friction = np.float64(0.1)
            drag = np.float64(0.91) * np.float64(0.6)
        else:
            friction = np.float64(0.02)
            drag = np.float64(0.91)

        self.move_flying(strafe, forward, friction)
        self.motion_y -= np.float64(0.08)
        self.move_entity(self.motion_x, self.motion_y, self.motion_z)

        self.motion_y *= np.float64(0.98)
        self.motion_x *= drag
        self.motion_z *= drag

    def on_update(self):
        self.on_entity_update()

    def on_entity_update(self):
        self.prev_distance_walked_modified = self.distance_walked_modified
        self.prev_pos_x = self.pos_x
        self.prev_pos_y = self.pos_y
        self.prev_pos_z = self.pos_z
        self.prev_rotation_pitch = self.rotation_pitch
        self.prev_rotation_yaw = self.rotation_yaw

        # self.handle_water_movement()

        # if self.is_in_lava():
        #     self.set_on_fire_from_lava()
        #     self.fall_distance *= np.float32(0.5)

        

    def on_living_update(self):
        if self.jump_ticks > 0:
            self.jump_ticks -= 1

        if abs(self.motion_y) < 0.005:
            self.motion_y = np.float64(0.0)

        if self.input.get_jump():
            if self.on_ground and self.jump_ticks == 0:
                self.jump()
                self.jump_ticks = 10
        else:
            self.jump_ticks = 0

        move_forward = (1.0 if self.input.get_forward() else 0.0) - (1.0 if self.input.get_backward() else 0.0)
        move_strafe = (1.0 if self.input.get_left() else 0.0) - (1.0 if self.input.get_right() else 0.0)
        self.move_entity_with_heading(move_strafe, move_forward)
