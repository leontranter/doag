from entity import get_blocking_entities_at_location
from game_states import GameStates

def attempt_move_entity(move, game_map, moving_entity, entities, game_state, player_turn_results, fov_recompute):
	dx, dy = move
	destination_x = moving_entity.x + dx
	destination_y = moving_entity.y + dy
	if not game_map.is_blocked(destination_x, destination_y):
		target = get_blocking_entities_at_location(entities, destination_x, destination_y)
		if target:
			attack_results = moving_entity.fighter.melee_attack(target)
			player_turn_results.extend(attack_results)
		else:	
			moving_entity.move(dx, dy)
			fov_recompute = True
		game_state = GameStates.ENEMY_TURN
	return player_turn_results, fov_recompute, game_state