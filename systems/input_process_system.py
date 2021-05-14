from systems import move_system
from systems import time_system
from systems.feat_system import attempt_feat
from systems.pickup_system import pickup_item
from game_states import GameStates
from game_messages import Message
from components.consumable import get_carried_potions
from fov_functions import initialize_fov, recompute_fov
from loader_functions.data_loaders import load_game, save_game
import tcod as libtcod
from systems import spell_system

def process_input(action, mouse_action, player, entities, game_state, message_log, game_map, dlevels, fov_recompute, fov_map, constants, con, targets):
	move, wait = action.get('move'), action.get('wait')
	pickup = action.get('pickup')
	show_inventory, drop_inventory = action.get('show_inventory'), action.get('drop_inventory')
	inventory_index = action.get('inventory_index')
	take_stairs, take_stairs_up = action.get('take_stairs'), action.get('take_stairs_up')
	show_character_screen = action.get('show_character_screen')
	show_skills_screen = action.get('show_skills_screen')
	exit = action.get('exit')
	fullscreen = action.get('fullscreen')
	equipment_screen = action.get('show_equipment_screen')
	spells_screen, spells_index = action.get('show_spells_screen'), action.get('spells_index')
	fire_weapon, load_weapon = action.get('fire_weapon'), action.get('load_weapon')
	potion_index = action.get('potion_index')
	quaff_potion = action.get('quaff_potion')
	feat_index = action.get('feat_index')
	perform_feat = action.get('perform_feat')

	left_click, right_click = mouse_action.get('left_click'), mouse_action.get('right_click')

	player_turn_results = []
	
	if move and game_state.current_game_state == GameStates.PLAYERS_TURN:
		player_turn_results, fov_recompute = move_system.attempt_move_entity(move, game_map, player, entities, player_turn_results, fov_recompute)

	elif wait:
		player_turn_results.append({'waited': True})

	elif pickup and game_state.current_game_state == GameStates.PLAYERS_TURN:
		player_turn_results.extend(pickup_item(player, entities))

	if show_inventory:
		game_state.previous_game_state = game_state.current_game_state
		game_state.current_game_state = GameStates.SHOW_INVENTORY
	if drop_inventory:
		game_state.previous_game_state = game_state.current_game_state
		game_state.current_game_state = GameStates.DROP_INVENTORY

	if equipment_screen:
		game_state.previous_game_state = game_state.current_game_state
		game_state.current_game_state = GameStates.EQUIPMENT_SCREEN

	if quaff_potion:
		game_state.previous_game_state = game_state.current_game_state
		game_state.current_game_state = GameStates.POTION_SCREEN

	if perform_feat:
		game_state.previous_game_state = game_state.current_game_state
		game_state.current_game_state = GameStates.FEATS_SCREEN

	if inventory_index is not None and game_state.previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
		item = player.inventory.items[inventory_index]
		if game_state.current_game_state == GameStates.SHOW_INVENTORY:
			player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
			game_state.current_game_state = GameStates.PLAYERS_TURN
			action_free = False
		elif game_state.current_game_state == GameStates.DROP_INVENTORY:
			player_turn_results.extend(player.inventory.drop_item(item))
			game_state.current_game_state = GameStates.PLAYERS_TURN

	if potion_index is not None and potion_index < len(get_carried_potions(player)):
		potions = get_carried_potions(player)
		used_potion = potions[potion_index]
		player_turn_results.extend(player.inventory.use(used_potion))

	# TODO: still needs some work
	if take_stairs and game_state == GameStates.PLAYERS_TURN:
		for entity in entities:
			if entity.stairs and entity.x == player.x and entity.y == player.y:
				entities, game_map.tiles, dlevels, game_map, player, fov_map, fov_recompute = game_map.down_stairs(entities, player, dlevels, game_map, fov_map, fov_recompute, constants)
				libtcod.console_clear(con)
		else:
			message_log.add_message(Message("There are no stairs here.", libtcod.yellow))

	if take_stairs_up and game_state == GameStates.PLAYERS_TURN:
		for entity in entities:
			if entity.stairs and entity.x == player.x and entity.y == player.y:
				if game_map.dungeon_level-1 in dlevels.keys():
					prev_level = dlevels[game_map.dungeon_level-1]
					entities, game_map.tiles, game_map.dungeon_level = prev_level.entities, prev_level.tiles, prev_level.floor
					for entity in entities:
						if entity.name.true_name == "Stairs":
							player.x, player.y = entity.x, entity.y
				else:
					entities = game_map.next_floor(player, message_log, constants, -1)	
				fov_map = initialize_fov(game_map)
				fov_recompute = True
				libtcod.console_clear(con)
				break
		else:
			message_log.add_message(Message("There are no up stairs here.", libtcod.yellow))

	if show_character_screen:
		game_state.previous_game_state = game_state.current_game_state
		game_state.current_game_state = GameStates.CHARACTER_SCREEN

	if show_skills_screen:
		game_state.previous_game_state = game_state.current_game_state
		game_state.current_game_state = GameStates.SKILLS_SCREEN		

	if spells_screen:
		game_state.previous_game_state = game_state
		game_state.current_game_state = GameStates.SPELLS_SCREEN

	if spells_index is not None and spells_index < len(player.caster.spells):
		spell = player.caster.spells[spells_index]
		player_turn_results.extend(spell_system.cast(player, spell, entities=entities, fov_map=fov_map))

	if feat_index is not None and feat_index < len(player.performer.feat_list):
		feat = player.performer.feat_list[feat_index]
		feat_index = None
		player_turn_results.extend(attempt_feat(player, feat, entities=entities, fov_map=fov_map))

	if fire_weapon:
		if player.equipment.ammunition and player.equipment.ammunition.item.quantity > 0:
			player_turn_results.extend(player.fighter.fire_weapon())
		else:
			player_turn_results.append({"message": Message("You don't have any ammunition to fire!")})

	if load_weapon:
		player_turn_results = player.fighter.load_missile_weapon()
		action_free = False

	if game_state.current_game_state == GameStates.TARGETING:
		if left_click:
			target_x, target_y = left_click
			if targets.current_targeting_consumable:	
				item_use_results = player.inventory.use(targets.current_targeting_consumable, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
				player_turn_results.extend(item_use_results)
			elif targets.current_targeting_spell:
				spell_use_results = spell_system.cast(player, targets.current_targeting_spell, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
				player_turn_results.extend(spell_use_results)	
			elif targets.current_targeting_feat:
				feat_perform_results = attempt_feat(player, targets.current_targeting_feat, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
				player_turn_results.extend(feat_perform_results)
			else:
				missile_attack_results = player.fighter.fire_weapon(weapon=player.equipment.main_hand.equippable, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
				player_turn_results.extend(missile_attack_results)
		elif right_click:
			player_turn_results.append({'targeting_cancelled': True})

	if exit:
		if game_state.current_game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN, GameStates.SPELLS_SCREEN, GameStates.POTION_SCREEN, GameStates.EQUIPMENT_SCREEN, GameStates.SKILLS_SCREEN):
			game_state.current_game_state = game_state.previous_game_state
		elif game_state.current_game_state == GameStates.TARGETING:
			player_turn_results.append({'targeting_cancelled': True})
		else:
			save_game(player, entities, game_map, message_log, game_state, dlevels)
			player_turn_results.append({'quit': True})

	if fullscreen:
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	return player_turn_results, fov_recompute, game_state, entities, game_map, fov_map, dlevels, targets