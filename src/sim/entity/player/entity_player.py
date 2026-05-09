import numpy as np

from src.sim.entity.player.entity_living_base import EntityLivingBase


class EntityPlayer(EntityLivingBase):
    def __init__(self):
        super().__init__()
        self.speed_in_air = np.float32(0.02)

    def on_update(self):
        super().on_update()

    def on_living_update():
        super().on_living_update()


