from src.sim.entity.player.entity_living_base import EntityLivingBase


class EntityPlayer(EntityLivingBase):
    def __init__(self):
        super().__init__()

    def on_update(self):
        super().on_update()
