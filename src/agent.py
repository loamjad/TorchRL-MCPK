from src.sim.client.entity.entity_player_sp import EntityPlayerSP

"""
An instance of a player in a Minecraft world.
"""
class Agent:
    def __init__(self):
        self.player = EntityPlayerSP()
        
    def run_tick(self):
        self.player.on_update()

    """
    Parameters:
    input_dict<String, bool>
        String - The input from w,a,s,d,jump,sprint,sneak
    """
    def set_inputs(self, input_dict):
        for key, value in input_dict.items():
            if not isinstance(value, bool):
                raise TypeError(f"Input '{key}' must be True or False, got {type(value).__name__}")
        settings = self.player.movement_input.game_settings
        settings.key_bind_forward.pressed = input_dict.get("w", False)
        settings.key_bind_left.pressed = input_dict.get("a", False)
        settings.key_bind_back.pressed = input_dict.get("s", False)
        settings.key_bind_right.pressed = input_dict.get("d", False)
        settings.key_bind_jump.pressed = input_dict.get("jump", False)
        settings.key_bind_sneak.pressed = input_dict.get("sneak", False)
        settings.key_bind_sprint.pressed = input_dict.get("sprint", False)

    def set_position(self, x, y, z):
        self.player.set_position(x, y, z)

    def get_pos(self):
        return (self.player.pos_x, self.player.pos_y, self.player.pos_z)

    def get_motion(self):
        return (self.player.motion_x, self.player.motion_y, self.player.motion_z)

    def get_rotation(self):
        return (self.player.rotation_yaw, self.player.rotation_pitch)

    def set_rotation(self, yaw, pitch):
        self.player.rotation_yaw = yaw
        self.player.rotation_pitch = pitch

    def get_last_tick_pos(self):
        return (self.player.last_tick_pos_x, self.player.last_tick_pos_y, self.player.last_tick_pos_z)
