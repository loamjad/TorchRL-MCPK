import numpy as np
import math

from src.sim.util.axis_aligned_bb import AxisAlignedBB
from src.sim.entity.data_watcher import DataWatcher
from src.sim.util.math_helper import MathHelper


class Entity:
    def __init__(self):
        ZERO_AABB = AxisAlignedBB(np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0), np.float64(0.0))

        self.world_obj = None

        self.bounding_box = ZERO_AABB
        self.width = np.float32(0.6)
        self.height = np.float32(1.8)
        self.nextStepDistance = 1
        self.set_position(np.float64(0.0), np.float64(0.0), np.float64(0.0))

        self.data_watcher = DataWatcher(self)
        self.data_watcher.add_object(0, np.int8(0))
        self.data_watcher.add_object(1, np.int16(300))
        self.data_watcher.add_object(3, np.int8(0))
        self.data_watcher.add_object(2, "")
        self.data_watcher.add_object(4, np.int8(0))

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

        self.prev_pos_x = np.float64(0.0)
        self.prev_pos_y = np.float64(0.0)
        self.prev_pos_z = np.float64(0.0)
        self.prev_rotation_yaw = np.float32(0.0)
        self.prev_rotation_pitch = np.float32(0.0)
        self.distance_walked_modified = np.float32(0.0)
        self.prev_distance_walked_modified = np.float32(0.0)

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

    def set_entity_bounding_box(self, bb: AxisAlignedBB):
        self.bounding_box = bb

    def get_jump_upwards_motion(self):
        return np.float32(0.42)

    def jump(self):
        self.motion_y = self.get_jump_upwards_motion()
        self.is_air_borne = True

    def move_entity(self, x, y, z):
        d0 = self.pos_x
        d1 = self.pos_y
        d2 = self.pos_z

        d3 = x
        d4 = y
        d5 = z
        flag = self.on_ground and self.is_sneaking

        if flag:
            d6 = np.float64(0.0)

        axisalignedbb = self.get_entity_bounding_box()

        self.set_entity_bounding_box(self.get_entity_bounding_box().offset(np.float64(0.0), y, np.float64(0.0)))

        self.set_entity_bounding_box(self.get_entity_bounding_box().offset(x, np.float64(0.0), np.float64(0.0)))

        self.set_entity_bounding_box(self.get_entity_bounding_box().offset(np.float64(0.0), np.float64(0.0), z))

        self.reset_position_to_BB()

    def move_flying(self, strafe, forward, friction):
        f = np.float32(strafe * strafe + forward * forward)

        if f >= np.float32(1.0E-4):
            f = MathHelper.sqrt_float(f)

            if f < np.float32(1.0):
                f = np.float32(1.0)

            f = friction / f
            strafe = strafe * f
            forward = forward * f
            f1 = MathHelper.sin(self.rotation_yaw * np.float32(math.pi) / np.float32(180.0))
            f2 = MathHelper.cos(self.rotation_yaw * np.float32(math.pi) / np.float32(180.0))
            self.motion_x += np.float64(strafe * f2 - forward * f1)
            self.motion_z += np.float64(forward * f2 + strafe * f1)

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
    
    def is_sneaking(self):
        return self.get_flag(1)
    
    def set_sneaking(self, sneaking):
        self.set_flag(1, sneaking)
    
    def is_sprinting(self):
        return self.get_flag(3)
    
    def set_sprinting(self, sprinting):
        self.set_flag(3, sprinting)
    
    def get_flag(self, flag):
        return self.data_watcher.get_watchable_object_byte(0) & 1 << flag != 0
    
    def set_flag(self, flag, set):
        b0 = self.data_watcher.get_watchable_object_byte(0)

        if set:
            self.data_watcher.update_object(0, np.int8(b0 | 1 << flag))
        else:
            self.data_watcher.update_object(0, np.int8(b0 & ~(1 << flag)))

    def get_entity_bounding_box(self):
        return self.bounding_box
    
    def set_entity_bounding_box(self, bb):
        self.bounding_box = bb

    def reset_position_to_BB(self):
        self.pos_x = (self.get_entity_bounding_box().min_x + self.get_entity_bounding_box().max_x) / np.float64(2.0)
        self.pos_y = self.get_entity_bounding_box().min_y
        self.pos_z = (self.get_entity_bounding_box().min_z + self.get_entity_bounding_box().max_z) / np.float64(2.0)