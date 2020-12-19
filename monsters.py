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
from systems.skill_manager import SkillNames

def getMonsterByDungeonLevel(level):
	pass

def make_orc(x, y):
	fighter_component = Fighter(xp_reward=2)
	stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	defender_component = Defender()
	skill_component = Skills()
	skill_component.set_skill_rank(SkillNames.SWORD, 1)
	skill_component.set_skill_rank(SkillNames.DAGGER, 1)
	orc_name = Name("Orc")
	monster = Entity(x, y, 'o', libtcod.red, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, ai=ai_component,
		equipment=equipment_component, stats=stats_component, skills=skill_component, defender=defender_component, name=orc_name)
	item = EquippableFactory.make_longsword()
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	item = EquippableFactory.make_leather_armor()
	monster.inventory.items.append(item)
	monster.equipment.body = item
	return monster

def make_troll(x, y):
	fighter_component = Fighter(xp_reward=4)
	stats_component = Stats(Strength=12, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	defender_component = Defender()
	skill_component = Skills()
	skill_component.set_skill_rank(SkillNames.SWORD, 1)
	skill_component.set_skill_rank(SkillNames.DAGGER, 1)
	troll_name = Name("Troll")
	monster = Entity(x, y, 't', libtcod.darker_green, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, ai=ai_component,
		equipment=equipment_component, stats=stats_component, skills=skill_component, defender=defender_component, name=troll_name)
	item = EquippableFactory.make_longsword()
	monster.inventory.items.append(item)
	monster.equipment.main_hand = item
	return monster

def make_kobold(x, y):
	fighter_component = Fighter(xp_reward=1)
	stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	ai_component = BasicMonster()
	equipment_component = Equipment()
	inventory_component = Inventory(26)
	defender_component = Defender()
	skill_component = Skills()
	skill_component.set_skill_rank(SkillNames.SWORD, 1)
	skill_component.set_skill_rank(SkillNames.DAGGER, 1)
	skill_component.set_skill_rank(SkillNames.BOW, 1)
	kobold_name = Name("Kobold")
	monster = Entity(x, y, 'k', libtcod.red, blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component, ai=ai_component,
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