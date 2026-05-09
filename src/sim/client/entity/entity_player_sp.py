from src.sim.client.entity.abstract_client_player import AbstractClientPlayer
from src.sim.util.movement_input_from_options import MovementInputFromOptions
from src.sim.client.settings.game_settings import GameSettings

class EntityPlayerSP(AbstractClientPlayer):

    def __init__(self):
        super().__init__()
        self.movement_input = MovementInputFromOptions(GameSettings)

    def on_living_update(self):
        # flag = self.movement_input.jump
        # flag1 = self.movement_input.sneak
        # f = np.float32(0.8)

        self.movement_input.update_player_move_state()
        super().on_living_update()

    def on_update(self):
        super().on_update()

    def update_entity_action_state(self):
        self.move_strafing = self.movement_input.move_strafe
        self.move_forward = self.movement_input.move_forward
        self.is_jumping = self.movement_input.jump

        super().update_entity_action_state()

        

