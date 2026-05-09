from src.sim.entity.entity import Entity


class EntityLivingBase(Entity):
    def __init__(self):
        super().__init__()
        self.jump_ticks = 0
    
    def on_update(self):
        self.last_tick_pos_x = self.pos_x
        self.last_tick_pos_y = self.pos_y
        self.last_tick_pos_z = self.pos_z
        self.on_living_update()
