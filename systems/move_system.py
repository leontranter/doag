import math
import tcod as libtcod
from game_states import GameStates
from systems.attack import attack
from attack_types import AttackTypes
from systems.effects_manager import is_confused
from random import randint

def attempt_move_entity(move, game_map, moving_entity, entities, player_turn_results, fov_recompute):
	if is_confused(moving_entity):
		dx, dy = (randint(0,1), randint(0,1))
		print(f'dx is {dx}, dy is {dy}')
		if (dx, dy) == (0, 0):
			player_turn_results.append({'waited': True})
			return player_turn_results, fov_recompute
	else:
		dx, dy = move
	destination_x = moving_entity.x + dx
	destination_y = moving_entity.y + dy
	if not game_map.is_blocked(destination_x, destination_y):
		target = get_blocking_entities_at_location(entities, destination_x, destination_y)
		if target:
			attack_results = attack(moving_entity, target, AttackTypes.MELEE)
			player_turn_results.extend(attack_results)
		else:	
			move_entity(moving_entity, dx, dy)
			fov_recompute = True
			player_turn_results.append({'moved': True})
	else:
		if is_confused(moving_entity):
			print("confused and bumped into a wall")
			player_turn_results.append({'waited': True})
	return player_turn_results, fov_recompute

def move_entity(moving_entity, dx, dy):
	moving_entity.x += dx
	moving_entity.y += dy

def move_astar(moving_entity, target, entities, game_map):
	# createa FOV map that has the dimensions of the map
	fov = libtcod.map_new(game_map.width, game_map.height)
	#scan the current map each turn and set all the walls as unwalkable
	for y1 in range(game_map.height):
		for x1 in range(game_map.width):
			libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].blocked)
	#scan all the objects to see if there are objects to be navigated around
	# check also that the object isn'tself or the target
	# the AI class handles the situation if the self is next to the target
	for entity in entities:
		if entity.blocks and entity != moving_entity and entity != target:
			#set the tile as a wall so it must be navigated around
			libtcod.map_set_properties(fov, entity.x, entity.y, True, False)
	# allocate a A* path
	# the 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
	my_path = libtcod.path_new_using_map(fov, 1.41)
	#compute the path between self's coordinates and target's coordinates
	libtcod.path_compute(my_path, moving_entity.x, moving_entity.y, target.x, target.y)
	#check if the path exists and the path is shorter than 25
	# path size matters if you want the monster to use alternative longer paths
	if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
		# find the next coordinates in the computed full path
		x, y, = libtcod.path_walk(my_path, True)
		if x or y:
			# set self's coordinates to the next path tile
			moving_entity.x = x
			moving_entity.y = y
	else:
		# keep the old move funtion as a backup so that if there are no paths
		# it will still try to move towards the player
		move_towards(moving_entity, target.x, target.y, game_map, entities)
	# delete the path to free memory
	libtcod.path_delete(my_path)

def move_towards(moving_entity, target_x, target_y, game_map, entities):
	dx = target_x - moving_entity.x
	dy = target_y - moving_entity.y
	distance = math.sqrt(dx ** 2 + dy ** 2)
	dx = int(round(dx / distance))
	dy = int(round(dy / distance))

	if not (game_map.is_blocked(moving_entity.x + dx, moving_entity.y + dy) or get_blocking_entities_at_location(entities, moving_entity.x + dx, moving_entity.y + dy)):
		move_entity(moving_entity, dx, dy)

def distance(moving_entity, x, y):
	return math.sqrt((x - moving_entity.x) ** 2 + (y - moving_entity.y) ** 2)

def distance_to(moving_entity, other_entity):
	dx = other_entity.x - moving_entity.x
	dy = other_entity.y - moving_entity.y
	return math.sqrt(dx ** 2 + dy ** 2)

def get_blocking_entities_at_location(entities, destination_x, destination_y):
	for entity in entities:
		if entity.blocks and entity.x == destination_x and entity.y == destination_y:
			return entity