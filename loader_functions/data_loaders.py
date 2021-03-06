import shelve
import os

def save_game(player, entities, game_map, message_log, game_state, dlevels):
	try:
		with shelve.open('savegame', 'n') as data_file:
			data_file['player_index'] = entities.index(player)
			data_file['entities'] = entities
			data_file['game_map'] = game_map
			data_file['message_log'] = message_log
			data_file['game_state'] = game_state
			data_file['dlevels'] = dlevels
			return True
	except:
		return False

def load_game():
	if not os.path.isfile('savegame.dat'):
		raise FileNotFoundError
	
	try:
		with shelve.open('savegame', 'r') as data_file:
			player_index = data_file['player_index']
			entities = data_file['entities']
			game_map = data_file['game_map']
			message_log = data_file['message_log']
			game_state = data_file['game_state']
			dlevels = data_file['dlevels']

		player = entities[player_index]

		return player, entities, game_map, message_log, game_state, dlevels
	except:
		return False