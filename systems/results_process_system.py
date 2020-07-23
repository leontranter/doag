from game_messages import Message
from game_states import GameStates
from death_functions import handle_death

def process_results(player_turn_results, game_state, previous_game_state, entities, player, targeting_item, missile_targeting, spell_targeting, message_log):
	for player_turn_result in player_turn_results:
		quit = player_turn_result.get('quit')
		message = player_turn_result.get('message')
		dead_entity = player_turn_result.get('dead')
		item_added = player_turn_result.get('item_added')
		item_consumed = player_turn_result.get('consumed')
		item_dropped = player_turn_result.get('item_dropped')
		targeting = player_turn_result.get('targeting')
		spell_targeting = player_turn_result.get('spell_targeting')
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
			game_state = GameStates.ENEMY_TURN
		if item_consumed:
			game_state = GameStates.ENEMY_TURN
		if fired_weapon:
			game_state = GameStates.ENEMY_TURN
		# TODO: roll these three results into one!
		if targeting:
			previous_game_state = GameStates.PLAYERS_TURN
			game_state = GameStates.TARGETING
			targeting_item = targeting
			message_log.add_message(targeting_item.consumable.targeting_message)
		if spell_targeting:
			previous_game_state = GameStates.PLAYERS_TURN
			game_state = GameStates.TARGETING
			message_log.add_message(spell_targeting.targeting_message)
		if missile_targeting:
			previous_game_state = GameStates.PLAYERS_TURN
			game_state = GameStates.TARGETING
			message_log.add_message(Message("Choose a target for your missile attack..."))
		if attack_miss or attack_defended:
			game_state = GameStates.ENEMY_TURN
		if missile_dropped:
			missile_entity = make_dropped_missile(missile_dropped, dropped_location)
			entities.append(missile_entity)
		if item_dropped:
			entities.append(item_dropped)
			game_state = GameStates.ENEMY_TURN
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
			game_state = GameStates.ENEMY_TURN
		if targeting_cancelled:
			game_state = previous_game_state
			message_log.add_message(Message('Targeting cancelled'))
		if cast:
			game_state = GameStates.ENEMY_TURN
		if loaded:
			game_state = GameStates.ENEMY_TURN

	return game_state, previous_game_state, entities