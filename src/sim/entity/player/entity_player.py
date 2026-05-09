import numpy as np

from src.sim.entity.player.entity_living_base import EntityLivingBase


class EntityPlayer(EntityLivingBase):
    def __init__(self):
        super().__init__()
        self.speed_in_air = np.float32(0.02)

    def on_update(self):
        super().on_update()

    def on_living_update(self):
        super().on_living_update()

        self.jump_movement_factor = self.speed_in_air

        if self.is_sprinting():
            self.jump_movement_factor = np.float32(np.float64(self.jump_movement_factor) + np.float64(self.speed_in_air) * np.float64(0.3))

        self.set_AI_move_speed(np.float64(0.10000000149011612))

    

