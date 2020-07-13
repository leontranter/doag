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
from components.name import Name
from components.effects import Effects


def getMonsterByDungeonLevel(level):
	pass

def makeOrc(x, y):
	fighter_component = Fighter(xp=35)
	stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	defender_component = Defender()
	effects_component = Effects()
	skill_component = Skills()
	skill_component.set_skill_rank("sword", 10)
	skill_component.set_skill_rank("dagger", 12)
	orc_name = Name("Orc")
	monster = Entity(x, y, 'o', libtcod.desaturated_green, blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, inventory=inventory_component, ai=ai_component,
		equipment=equipment_component, stats=stats_component, skills=skill_component, defender=defender_component, name=orc_name)
	item = EquippableFactory.make_longsword()
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	item = EquippableFactory.make_leather_armor()
	monster.inventory.items.append(item)
	monster.equipment.body = item
	return monster

def makeTroll(x, y):
	fighter_component = Fighter(xp=100)
	stats_component = Stats(Strength=11, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	defender_component = Defender()
	effects_component = Effects()
	skill_component = Skills()
	skill_component.set_skill_rank("sword", 13)
	skill_component.set_skill_rank("dagger", 12)
	troll_name = Name("Troll")
	monster = Entity(x, y, 't', libtcod.darker_green, "Troll", blocks=True, render_order=RenderOrder.ACTOR, fighter = fighter_component, inventory=inventory_component, ai=ai_component,
		equipment=equipment_component, stats=stats_component, skills=skill_component, defender=defender_component, name=troll_name)
	item = EquippableFactory.make_longsword()
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
	effects_component = Effects()
	skill_component = Skills()
	skill_component.set_skill_rank("sword", 10)
	skill_component.set_skill_rank("dagger", 10)
	skill_component.set_skill_rank("bow", 10)
	kobold_name = Name("Kobold")
	monster = Entity(x, y, 'k', libtcod.blue, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, ai=ai_component,
		equipment=equipment_component, stats=stats_component, skills=skill_component, defender=defender_component, name=kobold_name)
	item = EquippableFactory.make_dagger()
	monster.inventory.items.append(item)
	item = EquippableFactory.make_shortbow()
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	item = EquippableFactory.make_arrows(1, 1, 5)
	monster.inventory.items.append(item)
	monster.equipment.ammunition = item
	return monster