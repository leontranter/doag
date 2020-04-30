import tcod as libtcod

def handle_keys(key):
	key_char = chr(key.c)
	# Movement keys
	if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
		return {'move': (0, -1)}
	elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
		return {'move': (0, 1)}
	elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP4:
		return {'move': (-1, 0)}
	elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP6:
		return {'move': (1, 0)}
	elif key.vk == libtcod.KEY_KP7:
		return {'move': (-1,-1)}
	elif key.vk == libtcod.KEY_KP9:
		return {'move': (1, -1)}
	elif key.vk == libtcod.KEY_KP1:
		return {'move': (-1, 1)}
	elif key.vk == libtcod.KEY_KP3:
		return {'move': (1, 1)}
	if key.vk == libtcod.KEY_ENTER and key.lalt:
		return {'fullscreen': True}

	elif key.vk == libtcod.KEY_ESCAPE:
		#exit the game
		return {'exit': True}

	return {}