import tcod as libtcod
from entity import Entity
from components.fighter import Fighter
from components.caster import Caster
from components.ai import BasicMonster
from render_functions import RenderOrder
from components.equipment import Equipment
from components.inventory import Inventory
from components.equippable import EquippableFactory
from components.stats import Stats
from components.skills import Skills


def getMonsterByDungeonLevel(level):
	pass

def makeOrc(x, y):
	fighter_component = Fighter(xp=35)
	stats_component = Stats(ST=10, DX=11, IQ=10, HT=10)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	skill_component = Skills()
	skill_component.setSkill("sword", 12)
	skill_component.setSkill("dagger", 12)
	monster = Entity(x, y, 'o', libtcod.desaturated_green, "Orc", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, inventory=inventory_component, ai = ai_component, equipment=equipment_component, stats=stats_component, skills=skill_component)
	equippable_component = EquippableFactory.makeDagger()
	item = Entity(x, y, '(', libtcod.red, 'Dagger', equippable = equippable_component)
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	return monster

def makeTroll(x, y):
	fighter_component = Fighter(base_dr=1, xp=100)
	stats_components = Stats(ST=13, DX=11, IQ=10, HT=12)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	skill_component = Skills()
	skill_component.setSkill("sword", 13)
	skill_component.setSkill("dagger", 12)
	monster = Entity(x, y, 't', libtcod.darker_green, "Troll", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, inventory=inventory_component, ai = ai_component, equipment=equipment_component, stats=stats_component, skills=skill_component)
	equippable_component = EquippableFactory.makeSword()
	item = Entity(x, y, '(', libtcod.red, 'Sword', equippable = equippable_component)
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	return monster

def makeKobold(x, y):
	fighter_component = Fighter(xp=30)
	stats_component = Stats(ST=9, DX=12, IQ=10, HT=9)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	skill_component = Skills()
	skill_component.setSkill("sword", 10)
	skill_component.setSkill("dagger", 10)
	monster = Entity(x, y, 'k', libtcod.blue, "Kobold", blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, ai=ai_component, equipment=equipment_component, stats=stats_component, skills=skill_component)
	equippable_component = EquippableFactory.makeDagger()
	item = Entity(x, y, '(', libtcod.red, 'Dagger', equippable = equippable_component)
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	return monster