from components.consumable import ConsumableTypes

def get_display_name(player, named_entity):
	# TODO: fix this - pretty terrible! need to refactor items completely (urgh)
	if named_entity.consumable:
		if named_entity.consumable.consumable_type == ConsumableTypes.POTION:
		# Check if player has identified this or not
			if named_entity.name.true_name not in player.identified.identified_potions:
				display_name = player.identified.potion_links[named_entity.name.true_name]
			else:
				display_name = named_entity.name.true_name
		if named_entity.consumable.consumable_type == ConsumableTypes.SCROLL:
		# Check if player has identified this or not
			if named_entity.name.true_name not in player.identified.identified_scrolls:
				display_name = player.identified.scroll_links[named_entity.name.true_name]
			else:
				display_name = named_entity.name.true_name
		elif named_entity.consumable.consumable_type == ConsumableTypes.SPELLBOOK:
			display_name = named_entity.name.true_name
		return display_name

	if named_entity.equippable:
		display_name = named_entity.name.equippable_name
	else:
		display_name = named_entity.name.true_name
	
	if named_entity.item:
		if named_entity.item.quantity > 1:
			display_name = str(named_entity.item.quantity) + " " + display_name + "s"
	
	return display_name