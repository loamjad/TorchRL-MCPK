import pytest
from unittest.mock import MagicMock, call

from src.sim.client.entity.entity_player_sp import EntityPlayerSP
from src.sim.client.settings.game_settings import GameSettings

def make_player():
    player = EntityPlayerSP()
    return player

def set_pressed_keys(player, w, a, s, d, jump, sneak):
    settings = player.movement_input.game_settings()
    settings.key_bind_forward.pressed = w
    settings.key_bind_left.pressed = a
    settings.key_bind_back.pressed = s
    settings.key_bind_right.pressed = d
    settings.key_bind_jump.pressed = jump
    settings.key_bind_sneak.pressed = sneak
class TestOnLivingUpdate:
    def test_movement(self):
        player = make_player()
        player.on_ground = True
        set_pressed_keys(
            player, 
            True, 
            True, 
            False, 
            False, 
            True, 
            False)

        player.on_update()
        print(player.pos_z)
