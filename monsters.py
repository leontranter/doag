import tcod as libtcod
from entity import Entity
from components.fighter import Fighter
from components.caster import Caster
from components.ai import BasicMonster
from render_functions import RenderOrder


def getMonsterByDungeonLevel(level):
	pass

def makeOrc(x, y):
	fighter_component = Fighter(hp=20, defense=1, power=4, xp=35)
	ai_component = BasicMonster()
	monster = Entity(x, y, 'o', libtcod.desaturated_green, "Orc", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, ai = ai_component)
	return monster

def makeTroll(x, y):
	fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
	ai_component = BasicMonster()
	monster = Entity(x, y, 't', libtcod.darker_green, "Troll", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, ai = ai_component)
	return monster

def makeKobold(x, y):
	fighter_component = Fighter(hp=20, defense=0, power=3, xp=40)
	ai_component = BasicMonster()
	monster = Entity(x, y, 'k', libtcod.blue, "Kobold", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, ai = ai_component)
	return monster