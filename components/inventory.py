import tcod as libtcod
from game_messages import Message

class Inventory:
	def __init__(self, capacity):
		self.capacity = capacity
		self.items = []

	def add_item(self, item):
		results = []

		if len(self.items) >= self.capacity:
			results.append({
				'item_added': None,
				'message': Message('You cannot carry any more, your Inventory is full.', libtcod.yellow)
				})
		else:
			temp_display_name = item.name.display_name
			if item.equippable and item.equippable.quantity and item.equippable.quantity == 1:
				temp_display_name = temp_display_name[:-1]
			results.append({
				'item_added': item,
				'message': Message('You pick up the {0}!'.format(temp_display_name), libtcod.yellow)
			})
			for current_item in self.items:
				if current_item.name.display_name == item.name.display_name and current_item.equippable and current_item.equippable.quantity and current_item.equippable.quantity > 0:
					# Checking if we can stack this item with one already carried
					# TODO: This will need a LOT more work at some point... not a very clever check
					current_item.equippable.quantity += item.equippable.quantity
					break	
			else:
				self.items.append(item)
		return results

	def use(self, item_entity, **kwargs):
		results = []

		item_component = item_entity.item

		# TODO: Fix this up - need to clearly categories potions and scrolls and handle them accordingly
		if item_entity.name.true_name in potion_types and item_entity.name.true_name not in identified_potions:
			identified_potions.append(item_entity.name.true_name)


		if item_component.use_function is None:
			equippable_component = item_entity.equippable
			if equippable_component:
				results.append({'equip': item_entity})
			else:
				results.append({'message': Message('The {0} cannot be used'.format(item_entity.name.display_name), libtcod.yellow)})
		else:
			if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
				results.append({'targeting': item_entity})
			else:
				kwargs = {**item_component.function_kwargs, **kwargs}
				item_use_results = item_component.use_function(self.owner, **kwargs)

				for item_use_result in item_use_results:
					if item_use_result.get('consumed'):
						self.remove_item(item_entity)
				results.extend(item_use_results)

		return results

	def remove_item(self, item):
		self.items.remove(item)

	def drop_item(self, item):
		results = []

		if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
			self.owner.equipment.toggle_equip(item)
		item.x = self.owner.x
		item.y = self.owner.y

		self.remove_item(item)
		results.append({'item_dropped': item, 'message': Message(f"{self.owner.name.display_name} dropped the {item.name.display_name}", libtcod.yellow)})

		return results

	def drop_on_death(self, entities, monster):
		for item in self.items:
			# TODO - does the monster need to de-equip these items?? should this be part of the class or module??
			item.x, item.y = self.owner.x, self.owner.y
			entities.append(item)
		self.items = []
		return entities