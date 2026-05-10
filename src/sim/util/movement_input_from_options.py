import numpy as np

from src.sim.util.movement_input import MovementInput

class MovementInputFromOptions(MovementInput):

    def __init__(self, game_settings_in):
        self.game_settings = game_settings_in
        self.move_strafe = np.float32(0.0)
        self.move_forward = np.float32(0.0)
        self.jump = False
        self.sneak = False

    def update_player_move_state(self):
        self.move_strafe = np.float32(0.0)
        self.move_forward = np.float32(0.0)

        if self.game_settings.key_bind_forward.is_key_down():
            self.move_forward += np.float32(1.0)

        if self.game_settings.key_bind_back.is_key_down():
            self.move_forward -= np.float32(1.0)

        if self.game_settings.key_bind_left.is_key_down():
            self.move_strafe += np.float32(1.0)

        if self.game_settings.key_bind_right.is_key_down():
            self.move_strafe -= np.float32(1.0)


        self.jump = self.game_settings.key_bind_jump.is_key_down()
        self.sneak = self.game_settings.key_bind_sneak.is_key_down()

        if self.sneak:
            self.move_strafe = np.float32(self.move_strafe * np.float64(0.3))
            self.move_forward = np.float32(self.move_forward * np.float64(0.3))
