import numpy as np
from src.sim.entity.entity import Entity
from src.sim.util.math_helper import MathHelper

class EntityLivingBase(Entity):
    def __init__(self):
        super().__init__()
        self.is_jumping = False
        self.jump_ticks = 0
        self.move_strafing = np.float32(0.0)
        self.move_forward = np.float32(0.0)
        self.random_yaw_velocity = np.float32(0.0)
        self.jump_movement_factor = np.float32(0.02)
        self.step_height = np.float32(0.6)
    
    def is_sprinting(self) -> bool:
        return False

    def get_jump_upwards_motion(self) -> np.float32:
        return np.float32(0.42)

    def jump(self):
        self.motion_y = np.float64(self.get_jump_upwards_motion())

        if self.is_sprinting():
            f = self.rotation_yaw * np.float32(0.017453292)
            self.motion_x -= np.float64(MathHelper.sin(f) * np.float32(0.2))
            self.motion_z += np.float64(MathHelper.cos(f) * np.float32(0.2))

        self.is_air_borne = True

    def on_update():
        super.on_update()
        
        self.on_living_update()

    def on_living_update(self):
        threshold = np.float64(0.005)
        if np.abs(self.motion_x) < threshold:
            self.motion_x = np.float64(0.0)
        if np.abs(self.motion_y) < threshold:
            self.motion_y = np.float64(0.0)
        if np.abs(self.motion_z) < threshold:
            self.motion_z = np.float64(0.0)

        if self.is_jumping:
            if self.on_ground and self.jump_ticks == 0:
                self.jump()
                self.jump_ticks = 10
        else:
            self.jump_ticks = 0

        self.move_strafing = np.float32(self.move_strafing * np.float32(0.98))
        self.move_forward = np.float32(self.move_forward * np.float32(0.98))
        self.random_yaw_velocity = np.float32(self.random_yaw_velocity * np.float32(0.9))
        self.move_entity_with_heading(self.move_strafing, self.move_forward)

    def move_entity_with_heading(self, strafe, forward):
        f4 = np.float32(0.91)

        if self.on_ground:
            f4 = np.float32(1.0) # Needs Update

        f = np.float32(0.16277136) / (f4 * f4 * f4)

        if self.ground:
            pass
        else:
            pass

        return super().move_entity_with_heading(strafe, forward)