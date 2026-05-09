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
        self.land_movement_factor = np.float32(0.0)
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

    def on_update(self):
        super().on_update()
        
        self.on_living_update()

    def on_living_update(self):
        if self.jump_ticks > 0:
            self.jump_ticks -= 1

        # TODO: Is this needed?
        # self.motion_x *= np.float64(0.98)
        # self.motion_y *= np.float64(0.98)
        # self.motion_z *= np.float64(0.98)

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

        self.move_strafing *= np.float32(0.98)
        self.move_forward *= np.float32(0.98)
        self.random_yaw_velocity = np.float32(self.random_yaw_velocity * np.float32(0.9))
        self.move_entity_with_heading(self.move_strafing, self.move_forward)

    def move_entity_with_heading(self, strafe, forward):
        f4 = np.float32(0.91)

        if self.on_ground:
            f4 = np.float32(1.0) # TODO: Find value

        f = np.float32(0.16277136) / (f4 * f4 * f4)

        if self.on_ground:
            f5 = self.get_AI_move_speed() * f
        else:
            f5 = self.jump_movement_factor

        self.move_flying(strafe, forward, f5)
        f4 = np.float32(0.91)

        if self.on_ground:
            # TODO: f4 = this.worldObj.getBlockState(new BlockPos(MathHelper.floor_double(this.posX), MathHelper.floor_double(this.getEntityBoundingBox().minY) - 1, MathHelper.floor_double(this.posZ))).getBlock().slipperiness * 0.91F;
            pass

        self.move_entity(self.motion_x, self.motion_y, self.motion_z)

        if False: # TODO: this.worldObj.isRemote && (!this.worldObj.isBlockLoaded(new BlockPos((int)this.posX, 0, (int)this.posZ)) || !this.worldObj.getChunkFromBlockCoords(new BlockPos((int)this.posX, 0, (int)this.posZ)).isLoaded()))
            pass
        else:
            self.motion_y -= np.float64(0.08)

        self.motion_y *= np.float64(0.9800000190734863)
        self.motion_x *= np.float64(f4)
        self.motion_z *= np.float64(f4)
    
    def get_AI_move_speed(self):
        return self.land_movement_factor
    
    def set_AI_move_speed(self, speed_in):
        self.land_movement_factor = speed_in
