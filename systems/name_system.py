def get_display_name(player, named_entity):
	# TODO: fix this - pretty terrible! need to refactor items completely (urgh)
	if named_entity.item:
		if named_entity.item.use_function:
			# Check if player has identified this or not
			if named_entity.name.true_name not in player.identified.identified_potions:
				display_name = player.identified.potion_links[named_entity.name.true_name]
			else:
				display_name = named_entity.name.true_name
		if named_entity.equippable:
			# Fix this later
			display_name = named_entity.name.equippable_name
	else:
		display_name = named_entity.name.true_name
	return display_name