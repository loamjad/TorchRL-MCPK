from src.sim.client.settings.key_binding import KeyBinding

class GameSettings:
    def __init__(self):
        self.key_bind_forward = KeyBinding("key.forward", 17, "key.categories.movement")
        self.key_bind_left    = KeyBinding("key.left",    30, "key.categories.movement")
        self.key_bind_back    = KeyBinding("key.back",    31, "key.categories.movement")
        self.key_bind_right   = KeyBinding("key.right",   32, "key.categories.movement")
        self.key_bind_jump    = KeyBinding("key.jump",    57, "key.categories.movement")
        self.key_bind_sneak   = KeyBinding("key.sneak",   42, "key.categories.movement")
        self.key_bind_sprint  = KeyBinding("key.sprint",  29, "key.categories.movement")