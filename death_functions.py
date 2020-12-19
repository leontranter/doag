import tcod as libtcod
from game_states import GameStates
from render_functions import RenderOrder
from game_messages import Message
from loader_functions.tile_codes import *

def kill_player(player, game_state):
	player.char = '%'
	player.color = libtcod.dark_red
	game_state.current_game_state = GameStates.PLAYER_DEAD
	return Message('You died!', libtcod.red), game_state

def kill_monster(monster, player):
	death_message = Message('{0} is dead!'.format(monster.name.subject_name), libtcod.orange)

	player.fighter.unspent_xp += monster.fighter.xp_reward

	monster.char = CORPSE
	monster.color = libtcod.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	if monster.name.true_name[0].lower() in 'aeiou':
		monster.name.true_name = 'remains of an ' + monster.name.true_name
	else:
		monster.name.true_name = 'remains of a ' + monster.name.true_name
	monster.render_order = RenderOrder.CORPSE	

	return death_message, player

def handle_death(entities, dead_entity, player, game_state):
	if dead_entity == player:
		message, game_state = kill_player(dead_entity, game_state)
		print(game_state.current_game_state)
	else:
		message, player = kill_monster(dead_entity, player)
		entities = dead_entity.inventory.drop_on_death(entities, dead_entity)
	return message, game_state, entities