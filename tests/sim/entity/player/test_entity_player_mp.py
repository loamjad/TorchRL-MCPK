import numpy as np
import pytest

from src.sim.entity.player.entity_player_mp import EntityPlayerMP


def make_player():
    """Return a fresh EntityPlayerMP with on_ground=True and ground=False stub."""
    player = EntityPlayerMP()
    player.on_ground = True
    # 'ground' is referenced in move_entity_with_heading but not initialised by
    # any class in the hierarchy — set it here so the movement chain doesn't
    # raise AttributeError until that bug is fixed upstream.
    player.ground = False
    return player


class TestInit:
    def test_default_position_zero(self):
        player = EntityPlayerMP()
        assert player.pos_x == 0.0
        assert player.pos_y == 0.0
        assert player.pos_z == 0.0

    def test_default_motion_zero(self):
        player = EntityPlayerMP()
        assert player.motion_x == 0.0
        assert player.motion_y == 0.0
        assert player.motion_z == 0.0

    def test_default_rotation_zero(self):
        player = EntityPlayerMP()
        assert player.rotation_yaw == 0.0
        assert player.rotation_pitch == 0.0

    def test_default_on_ground_false(self):
        player = EntityPlayerMP()
        assert player.on_ground is False

    def test_player_dimensions(self):
        player = EntityPlayerMP()
        assert float(player.width) == pytest.approx(0.6, abs=1e-5)
        assert float(player.height) == pytest.approx(1.8, abs=1e-5)

    def test_speed_in_air(self):
        player = EntityPlayerMP()
        assert float(player.speed_in_air) == pytest.approx(0.02, abs=1e-5)


class TestSetPosition:
    def test_updates_coordinates(self):
        player = EntityPlayerMP()
        player.set_position(3.0, 5.0, -2.0)
        assert player.pos_x == pytest.approx(3.0)
        assert player.pos_y == pytest.approx(5.0)
        assert player.pos_z == pytest.approx(-2.0)

    def test_bounding_box_min_y_at_feet(self):
        player = EntityPlayerMP()
        player.set_position(0.0, 4.0, 0.0)
        assert player.bounding_box.min_y == pytest.approx(4.0)

    def test_bounding_box_max_y_at_head(self):
        player = EntityPlayerMP()
        player.set_position(0.0, 0.0, 0.0)
        assert player.bounding_box.max_y == pytest.approx(1.8, abs=1e-4)

    def test_bounding_box_width_centred_on_x(self):
        player = EntityPlayerMP()
        player.set_position(10.0, 0.0, 0.0)
        half = 0.6 / 2.0
        assert player.bounding_box.min_x == pytest.approx(10.0 - half, abs=1e-5)
        assert player.bounding_box.max_x == pytest.approx(10.0 + half, abs=1e-5)

    def test_bounding_box_width_centred_on_z(self):
        player = EntityPlayerMP()
        player.set_position(0.0, 0.0, 10.0)
        half = 0.6 / 2.0
        assert player.bounding_box.min_z == pytest.approx(10.0 - half, abs=1e-5)
        assert player.bounding_box.max_z == pytest.approx(10.0 + half, abs=1e-5)


class TestMoveEntity:
    def test_moves_position(self):
        player = EntityPlayerMP()
        player.move_entity(2.0, 1.0, -3.0)
        assert player.pos_x == pytest.approx(2.0)
        assert player.pos_y == pytest.approx(1.0)
        assert player.pos_z == pytest.approx(-3.0)

    def test_floor_clamps_y_to_zero(self):
        player = EntityPlayerMP()
        player.move_entity(0.0, -5.0, 0.0)
        assert player.pos_y == pytest.approx(0.0)

    def test_floor_collision_sets_on_ground(self):
        player = EntityPlayerMP()
        player.move_entity(0.0, -5.0, 0.0)
        assert player.on_ground is True

    def test_floor_collision_zeros_motion_y(self):
        player = EntityPlayerMP()
        player.motion_y = np.float64(-5.0)
        player.move_entity(0.0, -5.0, 0.0)
        assert player.motion_y == pytest.approx(0.0)

    def test_moving_up_clears_on_ground(self):
        player = EntityPlayerMP()
        player.on_ground = True
        player.move_entity(0.0, 1.0, 0.0)
        assert player.on_ground is False

    def test_accumulates_from_current_position(self):
        player = EntityPlayerMP()
        player.set_position(1.0, 0.0, 1.0)
        player.move_entity(2.0, 0.0, 3.0)
        assert player.pos_x == pytest.approx(3.0)
        assert player.pos_z == pytest.approx(4.0)


class TestJump:
    def test_sets_motion_y(self):
        player = EntityPlayerMP()
        player.jump()
        assert float(player.motion_y) == pytest.approx(0.42, abs=1e-5)

    def test_sets_is_air_borne(self):
        player = EntityPlayerMP()
        player.jump()
        assert player.is_air_borne is True


class TestOnEntityUpdate:
    def test_snapshots_prev_position(self):
        player = EntityPlayerMP()
        player.set_position(7.0, 3.0, -1.0)
        player.on_entity_update()
        assert player.prev_pos_x == pytest.approx(7.0)
        assert player.prev_pos_y == pytest.approx(3.0)
        assert player.prev_pos_z == pytest.approx(-1.0)

    def test_snapshots_prev_rotation(self):
        player = EntityPlayerMP()
        player.rotation_yaw = np.float32(90.0)
        player.rotation_pitch = np.float32(-30.0)
        player.on_entity_update()
        assert float(player.prev_rotation_yaw) == pytest.approx(90.0)
        assert float(player.prev_rotation_pitch) == pytest.approx(-30.0)


class TestOnUpdate:
    def test_prev_pos_reflects_position_before_tick(self):
        player = make_player()
        player.set_position(4.0, 0.0, 2.0)
        player.on_update()
        assert player.prev_pos_x == pytest.approx(4.0)
        assert player.prev_pos_z == pytest.approx(2.0)

    def test_gravity_pulls_motion_y_negative_when_airborne(self):
        player = make_player()
        player.on_ground = False
        player.motion_y = np.float64(0.0)
        player.on_update()
        assert player.motion_y < 0.0

    def test_motion_below_threshold_is_zeroed(self):
        player = make_player()
        player.motion_x = np.float64(0.001)
        player.motion_z = np.float64(0.001)
        player.on_update()
        assert player.motion_x == pytest.approx(0.0)
        assert player.motion_z == pytest.approx(0.0)

    def test_motion_above_threshold_is_kept(self):
        player = make_player()
        player.motion_x = np.float64(0.5)
        player.on_update()
        assert player.motion_x != pytest.approx(0.0)

    def test_jump_ticks_decremented(self):
        player = make_player()
        player.is_jumping = True
        player.jump_ticks = 5
        player.on_update()
        assert player.jump_ticks == 4

    def test_jump_triggered_when_on_ground_and_is_jumping(self):
        player = make_player()
        player.on_ground = True
        player.jump_ticks = 0
        player.is_jumping = True
        player.on_update()
        assert player.motion_y > 0.0

    def test_jump_not_triggered_when_airborne(self):
        player = make_player()
        player.on_ground = False
        player.jump_ticks = 0
        player.is_jumping = True
        player.motion_y = np.float64(0.0)
        player.on_update()
        assert player.motion_y <= 0.0

    def test_jump_blocked_during_jump_ticks_cooldown(self):
        player = make_player()
        player.on_ground = True
        player.jump_ticks = 5
        player.is_jumping = True
        player.motion_y = np.float64(0.0)
        player.on_update()
        assert player.motion_y <= 0.0
