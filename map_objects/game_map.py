from map_objects.tile import Tile
from map_objects.rectangle import Rect
from random import randint
import tcod as libtcod
import components.item
from entity import Entity
from components.fighter import Fighter
from components.ai import BasicMonster
from render_functions import RenderOrder
from components.item import Item
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.stairs import Stairs
from item_functions import cast_fireball, cast_lightning, heal, cast_confuse
from game_messages import Message
from random_utils import from_dungeon_level, random_choice_from_dict

class GameMap:
	def __init__(self, width, height, dungeon_level=1):
		self.width = width
		self.height = height
		self.tiles = self.initialize_tiles()
		self.dungeon_level = dungeon_level

	def initialize_tiles(self):
		tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

		return tiles

	def create_room(self, room):
		# go through the tiles in the rectangle and make them passable	
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.tiles[x][y].blocked = False
				#print("self.tiles for {},{} is blocked?".format(x, y))
				#print(self.is_blocked(x,y))
				self.tiles[x][y].block_sight = False

	def is_blocked(self, x, y):
		if self.tiles[x][y].blocked:
			return True

		return False

	def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, floor_direction=1):
		rooms = []
		num_rooms = 0

		center_of_last_room_x = None
		center_of_last_room_y = None

		for r in range(max_rooms):
			# random width and height
			w = randint(room_min_size, room_max_size)
			h = randint(room_min_size, room_max_size)
			# random position without going out of the map boundaries
			x = randint(0, map_width - w - 1)
			y = randint(0, map_height - h - 1)
			
			# Rect class makes rectangles easy
			new_room = Rect(x, y, w, h)

			# run through other rooms and see if they intersect with this one
			for other_room in rooms:
				if new_room.intersect(other_room):
					break
			else:
				# no intersections, the room is valid
				# paint it to the map's tiles
				self.create_room(new_room)
				
				#center coordinates of the room, will be useful later
				(new_x, new_y) = new_room.center()
				
				center_of_last_room_x = new_x
				center_of_last_room_y = new_y

				if num_rooms == 0:
					# this is the first room, where the player starts
					player.x = new_x
					player.y = new_y
				else:
					# for all other rooms, connect it to the previous room with a tunnel
					(prev_x, prev_y) = rooms[num_rooms -1].center()
					#flip a coin
					if randint(0,1) == 1:
						#first move horizontally then vertically
						self.create_h_tunnel(prev_x, new_x, prev_y)
						self.create_v_tunnel(prev_y, new_y, new_x)
					else:
						#first move vertically then horizontally
						self.create_v_tunnel(prev_y, new_y, prev_x)
						self.create_h_tunnel(prev_x, new_x, new_y)
				
				self.place_entities(new_room, entities)

				rooms.append(new_room)
				num_rooms += 1

		# create the down stairs
		stairs_component = Stairs(self.dungeon_level + 1)
		down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs', render_order=RenderOrder.STAIRS, stairs=stairs_component)
		if floor_direction == -1:
			down_stairs.x, down_stairs.y = player.x, player.y
		entities.append(down_stairs)

		# if this isn't level 1, create an up stairway
		if self.dungeon_level != 1:
			stairs_component_up = Stairs(self.dungeon_level - 1)
			up_stairs = Entity(player.x, player.y, '<', libtcod.white, 'Upward stairs', render_order=RenderOrder.STAIRS, stairs=stairs_component_up)
			entities.append(up_stairs)

	def create_h_tunnel(self, x1, x2, y):
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False

	def create_v_tunnel(self, y1, y2, x):
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False

	def place_entities(self, room, entities):
		# get a random number of monsters
		#max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
		max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
		max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
		number_of_monsters = randint(0, max_monsters_per_room)
		number_of_items = randint(0, max_items_per_room)

		monster_chances = {
			'orc': 80,
			'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
		}

		item_chances = {
			'healing_potion': 35,
			'armor': 20,
			'heal_book': 90,
			'sword': from_dungeon_level([[25, 1]], self.dungeon_level),
			'shield': from_dungeon_level([[25, 1]], self.dungeon_level),
			'lightning_scroll': from_dungeon_level([[25, 3]], self.dungeon_level),
			'fireball_scroll': from_dungeon_level([[25, 2]], self.dungeon_level),
			'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level)
		}

		for i in range(number_of_monsters):
			# choose a random location in the room
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)

			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				monster_choice = random_choice_from_dict(monster_chances)
				if monster_choice == 'orc':
					fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
					ai_component = BasicMonster()
					monster = Entity(x, y, 'o', libtcod.desaturated_green, "Orc", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, ai = ai_component)
				else:
					fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
					ai_component = BasicMonster()
					monster = Entity(x, y, 't', libtcod.darker_green, "Troll", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, ai = ai_component)
				entities.append(monster)

		for i in range(number_of_items):
			x = randint(room.x1 + 1, room.x2 - 1)
			y = randint(room.y1 + 1, room.y2 - 1)

			if not any([entity for entity in entities if entity.x == x and entity.y == y]):
				item_choice = random_choice_from_dict(item_chances)
				if item_choice == 'healing_potion':
					item_component = Item.makeHealingPotion()
					item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, item=item_component)
				elif item_choice == 'sword':
					equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
					item = Entity(x, y, '/', libtcod.sky, 'Sword', equippable=equippable_component)
				elif item_choice == 'shield':
					equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
					item = Entity(x, y, '/', libtcod.darker_orange, 'Shield', equippable=equippable_component)
				elif item_choice == 'armor':
					equippable_component = Equippable(EquipmentSlots.BODY, defense_bonus=2)
					item = Entity(x, y, '/', libtcod.darker_orange, 'Armor', equippable=equippable_component)
				elif item_choice == 'fireball_scroll':
					item_component = Item.makeFireballScroll()
					#item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan), damage=25, radius=3)
					item = Entity(x, y, '?', libtcod.red, 'Fireball scroll', render_order=RenderOrder.ITEM, item=item_component)
				elif item_choice == 'confusion_scroll':
					item_component = Item.makeConfusionScroll()
					#item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message('Left-click on an enemy to confuse it or right-click to cancel.', libtcod.light_cyan))
					item = Entity(x, y, '?', libtcod.light_pink, 'Confusion scroll', render_order=RenderOrder.ITEM, item=item_component)
				elif item_choice == 'fireball_book':
					item_component = Item.makeFireballBook()
					item = Entity(x, y, '#', libtcod.red, 'Fireball spellbook', render_order=RenderOrder.ITEM, item=item_component)
				elif item_choice == 'heal_book':
					item_component = Item.makeHealBook()
					item = Entity(x, y, '#', libtcod.red, 'Heal spellbook', render_order=RenderOrder.ITEM, item=item_component)
				else:
					item_component = Item.makeLightningScroll()
					#item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
					item = Entity(x, y, '?', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM, item=item_component)
				entities.append(item)

	def next_floor(self, player, message_log, constants, floor_direction):
		self.dungeon_level += floor_direction
		entities = [player]

		self.tiles = self.initialize_tiles()
		self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'], constants['map_height'], player, entities, floor_direction)
		
		player.fighter.heal(10)
		message_log.add_message(Message('You take a moment to rest and recover your strength.', libtcod.light_violet))

		return entities

	def save_floor(self, dlevels, entities):
		dlevels["dlevel_" + str(self.dungeon_level)].entities = entities
		dlevels["dlevel_" + str(self.dungeon_level)].tiles = self.tiles

	def load_floor(self, dlevels, dungeon_level):
		entities = dlevels[dungeon_level].entities
		tiles = dlevels[dungeon_level].tiles
		self.dungeon_level += 1
		return entities, tiles, self.dungeon_level