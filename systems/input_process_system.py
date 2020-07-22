from systems import move_system
from systems import time_system
from systems.pickup_system import pickup_item
from game_states import GameStates
from game_messages import Message
from components.consumable import get_carried_potions
from fov_functions import initialize_fov, recompute_fov
from loader_functions.data_loaders import load_game, save_game
import tcod as libtcod
from systems import spell_system


def process_input(action, mouse_action, player, entities, game_state, previous_game_state, message_log, game_map, dlevels, fov_recompute, fov_map, constants, con, targeting_item, spell_targeting, missile_targeting):
	move, wait = action.get('move'), action.get('wait')
	pickup = action.get('pickup')
	show_inventory, drop_inventory = action.get('show_inventory'), action.get('drop_inventory')
	inventory_index = action.get('inventory_index')
	take_stairs, take_stairs_up = action.get('take_stairs'), action.get('take_stairs_up')
	show_character_screen = action.get('show_character_screen')
	exit = action.get('exit')
	fullscreen = action.get('fullscreen')
	equipment_screen = action.get('show_equipment_screen')
	spells_screen, spells_index = action.get('show_spells_screen'), action.get('spells_index')
	fire_weapon, load_weapon = action.get('fire_weapon'), action.get('load_weapon')
	potion_index = action.get('potion_index')
	quaff_potion = action.get('quaff_potion')

	left_click, right_click = mouse_action.get('left_click'), mouse_action.get('right_click')

	player_turn_results = []

	if move and game_state == GameStates.PLAYERS_TURN:
		player_turn_results, fov_recompute, game_state = move_system.attempt_move_entity(move, game_map, player, entities, game_state, player_turn_results, fov_recompute)
		# TODO - terrible bug - turn gets processed even if move attempt is unsuccessful!!!!!!
		player_turn_results.extend(time_system.process_entity_turn(player))

	elif wait:
		player_turn_results.extend(time_system.process_entity_turn(player))
		game_state = GameStates.ENEMY_TURN

	elif pickup and game_state == GameStates.PLAYERS_TURN:
		player_turn_results.extend(pickup_item(player, entities))
		# TODO: Fix this! Potentially a lot of work
		for result in player_turn_results:
			if 'item-added' in result.keys():
				player_turn_results.extend(time_system.process_entity_turn(player))

	if show_inventory:
		previous_game_state = game_state
		game_state = GameStates.SHOW_INVENTORY
	if drop_inventory:
		previous_game_state = game_state
		game_state = GameStates.DROP_INVENTORY

	if equipment_screen:
		previous_game_state = game_state
		game_state = GameStates.EQUIPMENT_SCREEN

	if quaff_potion:
		previous_game_state = game_state
		game_state = GameStates.POTION_SCREEN

	if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
		item = player.inventory.items[inventory_index]
		if game_state == GameStates.SHOW_INVENTORY:
			player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
			player_turn_results.extend(time_system.process_entity_turn(player))
		elif game_state == GameStates.DROP_INVENTORY:
			player_turn_results.extend(player.inventory.drop_item(item))

	if potion_index is not None:
		potions = get_carried_potions(player)
		# TODO: this blows up if someone chooses a leter outside of index!! not good!! other menus probably do too?
		used_potion = potions[potion_index]
		player_turn_results.extend(player.inventory.use(used_potion))

	# TODO: still needs some work
	if take_stairs and game_state == GameStates.PLAYERS_TURN:
		for entity in entities:
			if entity.stairs and entity.x == player.x and entity.y == player.y:
				player_turn_results.append({'down_stairs': True})
		else:
			message_log.add_message(Message("There are no stairs here.", libtcod.yellow))

	if take_stairs_up and game_state == GameStates.PLAYERS_TURN:
		for entity in entities:
			if entity.stairs and entity.x == player.x and entity.y == player.y:
				# go up the stairs
				player_turn_results.append({'up_stairs': True})
		else:
			message_log.add_message(Message("There are no up stairs here.", libtcod.yellow))

	if show_character_screen:
		previous_game_state = game_state
		game_state = GameStates.CHARACTER_SCREEN

	if spells_screen:
		previous_game_state = game_state
		game_state = GameStates.SPELLS_SCREEN

	if spells_index is not None and spells_index < len(player.caster.spells):
		spell = player.caster.spells[spells_index]
		player_turn_results.extend(spell_system.cast(player, spell, entities=entities, fov_map=fov_map))
		player_turn_results.extend(time_system.process_entity_turn(player))

	if fire_weapon:
		if player.equipment.ammunition and player.equipment.ammunition.equippable.quantity > 0:
			player_turn_results.extend(player.fighter.fire_weapon())
			player_turn_results.extend(time_system.process_entity_turn(player))
		else:
			player_turn_results.append({"message": Message("You don't have any ammunition to fire!")})

	if load_weapon:
		player_turn_results = player.fighter.load_missile_weapon()
		player_turn_results.extend(time_system.process_entity_turn(player))

	if game_state == GameStates.TARGETING:
		# TODO: fix this up, ugly as all hell
		if left_click:
			target_x, target_y = left_click
			if targeting_item:	
				print("targeting item!")
				item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
				player_turn_results.extend(item_use_results)
			elif spell_targeting:
				spell_use_results = player.caster.cast(spell_targeting, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
				player_turn_results.extend(spell_use_results)
			elif missile_targeting:
				missile_attack_results = player.fighter.fire_weapon(weapon=player.equipment.main_hand.equippable, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
				player_turn_results.extend(missile_attack_results)	
			player_turn_results.extend(time_system.process_entity_turn(player))
		elif right_click:
			player_turn_results.append({'targeting_cancelled': True})

	if exit:
		if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN, GameStates.SPELLS_SCREEN):
			game_state = previous_game_state
		elif game_state == GameStates.TARGETING:
			player_turn_results.append({'targeting_cancelled': True})
		else:
			save_game(player, entities, game_map, message_log, game_state, dlevels)
			player_turn_results.append({'quit': True})

	if fullscreen:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	return player_turn_results, fov_recompute, game_state, previous_game_state, entities, game_map, fov_map