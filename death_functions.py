import tcod as libtcod
from game_states import GameStates
from render_functions import RenderOrder
from game_messages import Message

def kill_player(player):
	player.char = '%'
	player.color = libtcod.dark_red
	return Message('You died!', libtcod.red), GameStates.PLAYER_DEAD

def kill_monster(monster):
	death_message = Message('{0} is dead!'.format(monster.name.true_name), libtcod.orange)

	monster.char = '%'
	monster.color = libtcod.dark_red
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	if monster.name.true_name[0].lower() in 'aeiou':
		monster.name = 'remains of an ' + monster.name.true_name
	else:
		monster.name = 'remains of a ' + monster.name.true_name
	monster.render_order = RenderOrder.CORPSE	

	return death_message