def pickup_item(player, entities):
	player_turn_results = []
	for entity in entities:
		if entity.item and entity.x == player.x and entity.y == player.y:
			player_turn_results.extend(player.inventory.add_item(entity))
			break
	else:
		player_turn_results.append({'message': Message("There is nothing here to pick up.")})

	return player_turn_results