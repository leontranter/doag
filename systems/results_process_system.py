from game_messages import Message
from game_states import GameStates
from death_functions import handle_death
from components.equippable import make_dropped_missile
from death_functions import kill_player, kill_monster

def process_results(player_turn_results, game_state, previous_game_state, entities, player, message_log, targets):
	for player_turn_result in player_turn_results:
		quit = player_turn_result.get('quit')
		message = player_turn_result.get('message')
		dead_entity = player_turn_result.get('dead')
		item_added = player_turn_result.get('item_added')
		item_consumed = player_turn_result.get('consumed')
		item_dropped = player_turn_result.get('item_dropped')
		targeting = player_turn_result.get('targeting')
		spell_targeting_result = player_turn_result.get('spell_targeting')
		targeting_cancelled = player_turn_result.get('targeting_cancelled')
		equip = player_turn_result.get('equip')
		cast = player_turn_result.get('cast')
		missile_targeting = player_turn_result.get('missile_targeting')
		fired_weapon = player_turn_result.get("fired_weapon")
		attack_miss = player_turn_result.get("attack_miss")
		attack_defended = player_turn_result.get("attack_defended")
		missile_dropped = player_turn_result.get("missile_dropped")
		dropped_location = player_turn_result.get("dropped_location") 
		monster_drops = player_turn_result.get("monster_drops")
		loaded = player_turn_result.get("loaded")

		if quit:
			return True
		if message:
			message_log.add_message(message)
		if dead_entity:
			message, game_state, entities = handle_death(entities, dead_entity, player, game_state)
			message_log.add_message(message)
		if item_added:
			entities.remove(item_added)
		# TODO: delete these two?
		#if item_consumed:
		#	pass
		
		if fired_weapon:
			pass
		# TODO: roll these three results into one?
		if targeting:
			print("changing to targeting game state")
			previous_game_state = GameStates.PLAYERS_TURN
			game_state = GameStates.TARGETING
			targets.current_targeting_consumable = targeting
			print(f"targets item is {targets.current_targeting_consumable}")
			message_log.add_message(targets.current_targeting_consumable.consumable.targeting_message)
		if spell_targeting_result:
			previous_game_state = GameStates.PLAYERS_TURN
			game_state = GameStates.TARGETING
			targets.current_targeting_spell = spell_targeting_result
			message_log.add_message(player.fighter.currently_targeting_spell.targeting_message)
		if missile_targeting:
			previous_game_state = GameStates.PLAYERS_TURN
			game_state = GameStates.TARGETING
			targets.current_targeting_weapon = True
			message_log.add_message(Message("Choose a target for your missile attack..."))
		if attack_miss or attack_defended:
			pass
		if missile_dropped:
			missile_entity = make_dropped_missile(missile_dropped, dropped_location)
			entities.append(missile_entity)
		if item_dropped:
			entities.append(item_dropped)
			pass
		if equip:
			equip_results = player.equipment.toggle_equip(equip)
			for equip_result in equip_results:
				equipped = equip_result.get('equipped')
				dequipped = equip_result.get('dequipped')
				fail_equip = equip_result.get('fail_equip')
				if equipped:
					message_log.add_message(Message('You equipped the {0}.'.format(equipped.name.true_name)))
				if dequipped:
					message_log.add_message(Message('You dequipped the {0}.'.format(dequipped.name.true_name)))
				if fail_equip:
					message_log.add_message(Message(fail_equip))
			pass
		if targeting_cancelled:
			game_state = previous_game_state
			message_log.add_message(Message('Targeting cancelled'))
		# TODO: remove these?
		if cast:
			pass
		if loaded:
			pass

	return game_state, previous_game_state, entities, player, targets

def process_ai_results(enemy_turn_results, acting_entity, entities, player, message_log, game_state):
	for enemy_turn_result in enemy_turn_results:
		message = enemy_turn_result.get('message')
		dead_entity = enemy_turn_result.get('dead')
		missile_dropped = enemy_turn_result.get('missile_dropped')
		dropped_location = enemy_turn_result.get('dropped_location')
		equips = enemy_turn_result.get("equips")
		
		if message:
			message_log.add_message(message)
		if missile_dropped:
			missile_entity = make_dropped_missile(missile_dropped, dropped_location)
			entities.append(missile_entity)
		if equips:
			acting_entity.equipment.toggle_equip(equips)
		if dead_entity:
			if dead_entity == player:
				message, game_state = kill_player(dead_entity)
			else:
				message = kill_monster(dead_entity)
			message_log.add_message(message)
			if game_state == GameStates.PLAYER_DEAD:
				break

	return entities, game_state, message_log