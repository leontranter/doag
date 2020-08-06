import tcod as libtcod
from game_messages import Message
from loader_functions import constants
from systems.name_system import get_display_name
from components.consumable import ConsumableTypes

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
			temp_display_name = get_display_name(self.owner, item)
			if item.equippable and item.item.quantity and item.item.quantity == 1:
				temp_display_name = temp_display_name[:-1]
			results.append({
				'item_added': item,
				'message': Message('You pick up the {0}!'.format(temp_display_name), libtcod.yellow)
			})
			for current_item in self.items:
				if current_item.name.true_name == item.name.true_name and current_item.equippable and current_item.equippable.quantity and current_item.equippable.quantity > 0:
					# Checking if we can stack this item with one already carried
					# TODO: This will need a LOT more work at some point... not a very clever check
					current_item.equippable.quantity += item.equippable.quantity
					break	
			else:
				self.items.append(item)
		return results

	def use(self, item_entity, **kwargs):
		results = []
		game_constants = constants.get_constants()

		# identify the potion or scroll if it is unidentified
		if self.owner.identified and item_entity.consumable:
			# identify potion
			if item_entity.consumable.consumable_type == ConsumableTypes.POTION:
				if item_entity.name.true_name in game_constants["potion_types"] and item_entity.name.true_name not in self.owner.identified.identified_potions:
					self.owner.identified.identified_potions.append(item_entity.name.true_name)
			# identify scroll
			elif item_entity.consumable.consumable_type == ConsumableTypes.SCROLL:
				if item_entity.name.true_name in game_constants["scroll_types"] and item_entity.name.true_name not in self.owner.identified.identified_scrolls:
					self.owner.identified.identified_scrolls.append(item_entity.name.true_name)
		# TODO: Fix this, the logic sucks
		if not item_entity.consumable:
			equippable_component = item_entity.equippable
			if equippable_component:
				results.append({'equip': item_entity})
			else:
				results.append({'message': Message('The {0} cannot be used'.format(item_entity.name.true_name), libtcod.yellow)})
		else:
			if item_entity.consumable.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
				results.append({'targeting': item_entity})
			else:
				kwargs = {**item_entity.consumable.function_kwargs, **kwargs}
				item_use_results = item_entity.consumable.use_function(self.owner, **kwargs)

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
		results.append({'item_dropped': item, 'message': Message(f"{self.owner.name.subject_name} dropped the {get_display_name(self.owner, item)}", libtcod.yellow)})

		return results

	def drop_on_death(self, entities, monster):
		for item in self.items:
			# TODO - does the monster need to de-equip these items?? should this be part of the class or module??
			item.x, item.y = self.owner.x, self.owner.y
			entities.append(item)
		self.items = []
		return entities