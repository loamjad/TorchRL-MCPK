import numpy as np
import uuid

from src.sim.entity.entity import Entity
from src.sim.util.math_helper import MathHelper
from src.sim.util.block_pos import BlockPos
from src.sim.entity.ai.attributes.serverside_attribute_map import ServersideAttributeMap
from src.sim.entity.ai.attributes.attribute_modifier import AttributeModifier
from src.sim.entity.shared_monster_attributes import SharedMonsterAttributes


class EntityLivingBase(Entity):
    def __init__(self):
        super().__init__()
        self.attribute_map = None
        self.sprinting_speed_boost_modifier_UUID = uuid.UUID("662A6B8D-DA3E-4C1C-8813-96EA6097278D")
        self.sprinting_speed_boost_modifier = AttributeModifier(self.sprinting_speed_boost_modifier_UUID, "Sprinting spped boost", np.float64(0.30000001192092896), 2).set_saved(False)
        
        self.apply_entity_attributes()
        self.is_jumping = False
        self.jump_ticks = 0
        self.move_strafing = np.float32(0.0)
        self.move_forward = np.float32(0.0)
        self.random_yaw_velocity = np.float32(0.0)
        self.jump_movement_factor = np.float32(0.02)
        self.land_movement_factor = np.float64(0.10000000149011612)
        self.step_height = np.float32(0.6)

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

        threshold = np.float64(0.005)
        if np.abs(self.motion_x) < threshold:
            self.motion_x = np.float64(0.0)
        if np.abs(self.motion_y) < threshold:
            self.motion_y = np.float64(0.0)
        if np.abs(self.motion_z) < threshold:
            self.motion_z = np.float64(0.0)

        self.update_entity_action_state() # TODO: Remove this?

        if self.is_jumping:
            if self.on_ground and self.jump_ticks == 0:
                self.jump()
                self.jump_ticks = 10
        else:
            self.jump_ticks = 0

        self.move_strafing *= np.float32(0.98)
        self.move_forward *= np.float32(0.98)
        self.random_yaw_velocity *= np.float32(0.9)
        self.move_entity_with_heading(self.move_strafing, self.move_forward)

    def move_entity_with_heading(self, strafe, forward):
        f4 = np.float32(0.91)

        # if self.on_ground:
        #     f4 = self.world_obj.get_block_state(
        #         BlockPos(
        #             MathHelper.floor_double(self.pos_x),
        #             MathHelper.floor_double(self.get_entity_bounding_box().min_y) - 1,
        #             MathHelper.floor_double(self.pos_z)
        #             )
        #     ).get_block().slipperiness * np.float32(0.91)

        f4 = np.float32(0.6) * np.float32(0.91) # TODO: Remove once implement above

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

        self.motion_y -= np.float64(0.08)

        self.motion_y *= np.float64(0.9800000190734863)
        self.motion_x *= np.float64(f4)
        self.motion_z *= np.float64(f4)
    
    def get_AI_move_speed(self):
        return np.float32(self.get_entity_attribute(SharedMonsterAttributes.movement_speed).get_attribute_value())
    
    def set_AI_move_speed(self, speed_in):
        self.land_movement_factor = speed_in

    def update_entity_action_state(self):
        pass

    def set_sprinting(self, sprinting):
        super().set_sprinting(sprinting)
        iattributeinstance = self.get_entity_attribute(SharedMonsterAttributes.movement_speed)

        if sprinting:
            iattributeinstance.apply_modifier(self.sprinting_speed_boost_modifier)
    
    def get_entity_attribute(self, attribute):
        return self.get_attribute_map().get_attribute_instance(attribute)
    
    def get_attribute_map(self):
        if self.attribute_map == None:
            self.attribute_map = ServersideAttributeMap()

        return self.attribute_map
    
    def apply_entity_attributes(self):
        self.get_attribute_map().register_attribute(SharedMonsterAttributes.movement_speed)