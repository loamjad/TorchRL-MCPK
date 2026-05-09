from src.sim.entity.player.entity_player import EntityPlayer


class EntityPlayerMP(EntityPlayer):
    def __init__(self):
        super().__init__()

    def on_update(self):
        super().on_update()
