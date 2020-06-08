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
from components.defender import Defender


def getMonsterByDungeonLevel(level):
	pass

def makeOrc(x, y):
	fighter_component = Fighter(xp=35)
	stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	defender_component = Defender()
	skill_component = Skills()
	skill_component.set_skill_rank("sword", 10)
	skill_component.set_skill_rank("dagger", 12)
	monster = Entity(x, y, 'o', libtcod.desaturated_green, "Orc", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, inventory=inventory_component, ai = ai_component, equipment=equipment_component, stats=stats_component, skills=skill_component, defender=defender_component)
	item = EquippableFactory.makeBroadSword()
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	item = EquippableFactory.makeLeatherArmor()
	monster.inventory.items.append(item)
	monster.equipment.body = item
	return monster

def makeTroll(x, y):
	fighter_component = Fighter(base_dr=1, xp=100)
	stats_components = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	defender_component = Defender()
	skill_component = Skills()
	skill_component.set_skill_rank("sword", 13)
	skill_component.set_skill_rank("dagger", 12)
	monster = Entity(x, y, 't', libtcod.darker_green, "Troll", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, inventory=inventory_component, ai = ai_component, equipment=equipment_component, stats=stats_component, skills=skill_component, defender=defender_component)
	item = EquippableFactory.makeBroadSword()
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	return monster

def makeKobold(x, y):
	fighter_component = Fighter(xp=30)
	stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	defender_component = Defender()
	skill_component = Skills()
	skill_component.set_skill_rank("sword", 10)
	skill_component.set_skill_rank("dagger", 10)
	monster = Entity(x, y, 'k', libtcod.blue, "Kobold", blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, ai=ai_component, equipment=equipment_component, stats=stats_component, skills=skill_component, defender=defender_component)
	item = EquippableFactory.makeDagger()
	monster.inventory.items.append(item)
	item = EquippableFactory.makeBow()
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	item = EquippableFactory.makeArrows(quantity=5)
	monster.inventory.items.append(item)
	monster.equipment.ammunition = item
	return monster