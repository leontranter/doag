import tcod as libtcod
import components.equipment
from menu_options import MenuOption
from systems.name_system import get_display_name
from components.consumable import get_carried_potions
from systems.damage import get_damage_string
from systems.attack import weapon_skill_lookup, get_weapon_skill_for_attack
from equipment_slots import EquipmentSlots

def inventory_menu(con, header, inventory_width, screen_width, screen_height, player=None):
	# show a menu with each item of the inventory as an option
	if len(player.inventory.items) == 0:
		header = "Your inventory is empty."
	
	options = []
	for item in player.inventory.items:
		option_text = get_display_name(player, item)
		option_text = mark_equipped(option_text, item, player)
		options.append(" " + option_text)
	
	menu(con, header, options, inventory_width, screen_width, screen_height)

def spells_menu(con, header, spells_width, screen_width, screen_height, player):
	if len(player.caster.spells) == 0:
		header = "You don't know any spells yet."
	options = []
	for spell in player.caster.spells:
		options.append(spell.name)

	menu(con, header, options, spells_width, screen_width, screen_height)

def feats_menu(con, header, spells_width, screen_width, screen_height, player):
	if not player.performer:
		return None
	if len(player.performer.feat_list) == 0:
		header = "You don't know any feats yet."
	options = []
	for feat in player.performer.feat_list:
		options.append(feat.display_name)

	menu(con, header, options, spells_width, screen_width, screen_height)

def potion_menu(con, header, menu_width, screen_width, screen_height, player):
	potions = get_carried_potions(player)
	options = []
	for potion in potions:
		options.append(get_display_name(player, potion))
	menu(con, header, options, menu_width, screen_width, screen_height)

def get_equipped_items(entity):
	equipped_items = []
	equipped_items.append("Main hand: " + (entity.equipment.main_hand.name.true_name if entity.equipment.main_hand else ""))
	equipped_items.append("Off hand: " + (entity.equipment.off_hand.name.true_name if entity.equipment.off_hand else ""))
	equipped_items.append("Body: " + (entity.equipment.body.name.true_name if entity.equipment.body else ""))
	equipped_items.append("Ammunition: " + (get_display_name(entity, entity.equipment.ammunition) if entity.equipment.ammunition else ""))
	return equipped_items

def equipment_menu(con, header, menu_width, screen_width, screen_height, player):
	options = get_equipped_items(player)
	menu(con, header, options, menu_width, screen_width, screen_height)

def main_menu(con, backgrond_image, screen_width, screen_height):
	libtcod.image_blit_2x(backgrond_image, 0, 0, 0)

	libtcod.console_set_default_foreground(0, libtcod.light_yellow)
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) -4, libtcod.BKGND_NONE, libtcod.CENTER, 'TOMBS OF THE ANCIENT KINGS')
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height /2) -3, libtcod.BKGND_NONE, libtcod.CENTER, 'By Leon Tranter')
	options = ['Play a new game', 'Continue a game', 'Quit']	
	menu(con, '', options, 24, screen_width, screen_height)

def character_class_menu(con, screen_width, screen_height):
	libtcod.console_set_default_foreground(0, libtcod.light_yellow)
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) -4, libtcod.BKGND_NONE, libtcod.CENTER, 'TOMBS OF THE ANCIENT KINGS')
	libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height /2) -3, libtcod.BKGND_NONE, libtcod.CENTER, 'By Leon Tranter')
	options = ['a: Barbarian', 'b: Paladin', 'c: Wizard']	
	menu(con, '', options, 24, screen_width, screen_height)

def skills_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
	window = libtcod.console_new(character_screen_width, character_screen_height)
	libtcod.console_set_default_foreground(window, libtcod.cyan)
	
	libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Player Skills')
	libtcod.console_set_default_foreground(window, libtcod.white)
	offset = 3
	for skill in player.skills.skills:
		libtcod.console_print_rect_ex(window, 0, offset, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, f'{skill.name.capitalize()}: {player.skills.skills.get(skill)}')
		offset += 1
	x = screen_width // 2 - character_screen_width // 2
	y = screen_height // 2 - character_screen_height // 2

	libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

def message_box(con, header, width, screen_width, screen_height):
	menu2(con, header, [], width, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
	options = ['Constitution (+20HP)', 'Strength (+1 attack)', 'Agility (+1 defense)']

	menu(con, header, options, menu_width, screen_width, screen_height)

def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
	window = libtcod.console_new(character_screen_width, character_screen_height)
	libtcod.console_set_default_foreground(window, libtcod.white)
	damage_string = get_damage_string(player)
	weapon_string = str(weapon_skill_lookup(player.equipment.main_hand).name.lower())
	weapon_skill_string = str(get_weapon_skill_for_attack(player))

	libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Character Information')
	libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
	libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
	libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Experience to Level: {0}'.format(player.level.experience_to_next_level))
	libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Maximum HP: {0}'.format(player.stats.max_hp))
	libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Melee Damage: ' + damage_string)
	libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Current weapon skill used: ' + weapon_string)
	libtcod.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Current weapon skill check: ' + weapon_skill_string)
	libtcod.console_print_rect_ex(window, 0, 10, character_screen_width, character_screen_height, libtcod.BKGND_NONE, libtcod.LEFT, 'Damage Resistance: {0}'.format(player.fighter.DR))

	x = screen_width // 2 - character_screen_width // 2
	y = screen_height // 2 - character_screen_height // 2

	libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

def mark_equipped(text, option, player):
	if player.equipment.main_hand == option:
		text += " - main hand"
	if player.equipment.off_hand == option:
		text += " - off-hand"
	if player.equipment.body == option:
		text += " - worn on body"
	if player.equipment.ammunition == option:
		ammunition_name = player.equipment.ammunition.name.true_name
		if player.equipment.ammunition.equippable.quantity == 1:
			ammunition_name = display_name[:-1]
		text += " in quiver, {} {} left".format(player.equipment.ammunition.equippable.quantity, ammunition_name)
	return text

def menu(con, header, options, width, screen_width, screen_height):
	if len(options) > 26:
		raise ValueError('Cannot have a menu with more than 26 options!')

	# calculate total height for the header and one line per option
	header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
	height = len(options) + header_height

	# create an off-screen console that represent's the menu's window
	window = libtcod.console_new(width, height)

	# print the header, with autowrap
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	y = header_height
	letter_index = ord('a')
	
	for option in options:
		text = '(' + chr(letter_index) + ')' + option
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		letter_index += 1

	# blit the contents of "window" to the console
	x = int(screen_width / 2 - width / 2)
	y = int(screen_height / 2 - height / 2)
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)