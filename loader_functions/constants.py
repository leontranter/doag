import tcod as libtcod
from enum import Enum, auto

def get_constants():
	window_title = "Roguelike Tutorial Revised"

	screen_width = 90
	screen_height = 60

	bar_width = 20
	panel_height = 17
	panel_y = screen_height - panel_height

	message_x = bar_width + 2
	message_width = screen_width - bar_width - 2
	message_height = panel_height - 1

	max_dlevels = 6

	map_width = 80
	map_height = 43

	room_max_size = 10
	room_min_size = 6
	max_rooms = 10
	max_monsters_per_room = 3
	max_items_per_room = 2

	fov_algorithm = 0
	fov_light_walls = True
	fov_radius = 10
	
	potion_descriptions = ["dark potion", "fizzy potion", "cloudy potion"]
	potion_types = ["Healing Potion", "Poison Potion", "Confusion Potion"]
	
	scroll_descriptions = ["dusty scroll", "faded scroll"]
	scroll_types = ['Confusion Scroll', 'Fireball Scroll']

	character_classes = ["Barbarian", "Paladin", "Wizard", "Priest"]
	character_races = ["Dwarf", "Elf", "Fairy", "Moleperson", "Lizardkin", "Gnome", "Ogre", "Dark elf", "Iron dwarf", "Wildling"]

	colors = {
		'dark_wall': libtcod.Color(0, 0, 100),
		'dark_ground': libtcod.Color(50, 50, 150),
		'light_wall': libtcod.Color(130, 110, 50),
		'light_ground': libtcod.Color(200, 180, 50)
	}

	constants = {
		'window_title': window_title,
		'screen_width': screen_width,
		'screen_height': screen_height,
		'bar_width': bar_width,
		'panel_height': panel_height,
		'panel_y': panel_y,
		'message_x': message_x,
    	'message_width': message_width,
		'message_height': message_height,
		'map_width': map_width,
		'map_height': map_height,
		'room_max_size': room_max_size,
		'room_min_size': room_min_size,
		'max_rooms': max_rooms,
		'fov_algorithm': fov_algorithm,
		'fov_light_walls': fov_light_walls,
		'fov_radius': fov_radius,
		'max_monsters_per_room': max_monsters_per_room,
		'max_items_per_room': max_items_per_room,
		'colors': colors,
		'potion_descriptions': potion_descriptions,
		'potion_types': potion_types,
		'scroll_descriptions': scroll_descriptions,
		'scroll_types': scroll_types,
		'character_classes': character_classes,
		'character_races': character_races,
		'max_dlevels': max_dlevels
	}

	return constants

potion_descriptions = ["dark", "fizzy", "cloudy"]
potion_types = ["Healing Potion", "Poison Potion", "Confusion Potion"]

class WeaponTypes(Enum):
	DAGGER = auto()
	STILLETO = auto()
	LONGSWORD = auto()
	RAPIER = auto()
	SABER = auto()
	GREATSWORD = auto()
	CLUB = auto()
	MACE = auto()
	FLAIL = auto()
	MAUL = auto()
	SHORTBOW = auto()
	LONGBOW = auto()
	CROSSBOW = auto()
	HEAVY_CROSSBOW = auto()
	AXE = auto()
	GREATAXE = auto()
	STAFF = auto()
	WARSTAFF = auto()

class WeaponCategories(Enum):
	DAGGER = auto()
	SWORD = auto()
	BOW = auto()
	CROSSBOW = auto()
	AXE = auto()
	STAFF = auto()
	MACE = auto()

class AmmunitionTypes(Enum):
	ARROWS = auto()
	BOLTS = auto()