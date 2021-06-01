from menus import character_class_menu, main_menu
from input_handlers import handle_character_class_menu
import tcod as libtcod

def get_character_class(con, constants):
	key = libtcod.Key()
	mouse = libtcod.Mouse()
	character_class = None
	while not character_class:
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
		character_class_menu(con, constants['screen_width'], constants['screen_height'])
		libtcod.console_flush()
		character_class = handle_character_class_menu(key)
	return character_class