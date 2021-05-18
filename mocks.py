import tcod as libtcod
from components.fighter import Fighter
from components.caster import Caster
from components.equipment import Equipment
from components.equippable import Equippable, EquippableFactory
from components.skills import Skills
from components.stats import Stats
from components.defender import Defender
from components.name import Name
from components.identified import Identified
from components.inventory import Inventory
from entity import Entity
from systems.skill_manager import SkillNames
from components.level import Level

def create_mockchar_1():
	# basic stats, no skills or equipment, can identify stuff
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_identified = Identified()
	test_inventory = Inventory(10)
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", inventory=test_inventory, skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component, identified=test_identified)
	return test_entity

def create_mockchar_2():
	# basic stats and skills, no equipment
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.set_skill_rank(SkillNames.SWORD, 1)
	test_skills_component.set_skill_rank(SkillNames.SHIELD, 12)
	return test_entity

def create_mockchar_3():
	# stats and skills and a sword, no shield skill or equipped
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_item_entity = EquippableFactory.make_longsword()
	test_equipment_component.main_hand = test_item_entity
	test_fighter = Fighter()
	test_name = Name("Mock")
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component, fighter=test_fighter, name=test_name)	
	test_skills_component.set_skill_rank(SkillNames.SWORD, 1)
	return test_entity

def create_mockchar_4():
	# stats and skills and a sword, shield skill, has a shield but no shield equipped
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_shield = EquippableFactory.make_shield()
	test_sword = EquippableFactory.make_longsword()
	test_equipment_component.main_hand = test_sword	
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.set_skill_rank(SkillNames.SWORD, 14)
	return test_entity

def create_mockchar_5():
	# stats and skills and a sword and shield skill and shield equipped, better at sword than shield
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_fighter_component = Fighter()
	test_shield = EquippableFactory.make_shield()
	test_sword = EquippableFactory.make_longsword()
	test_equipment_component.main_hand = test_sword
	test_equipment_component.off_hand = test_shield	
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component, fighter=test_fighter_component)
	test_skills_component.set_skill_rank(SkillNames.SWORD, 1)
	test_skills_component.set_skill_rank(SkillNames.SHIELD, 1)
	return test_entity	

def create_mockchar_6():
	# stats and skills and a sword and shield skill, better at shield than sword, and shield equipped
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_shield = EquippableFactory.make_shield()
	test_sword = EquippableFactory.make_longsword()
	test_equipment_component.main_hand = test_sword
	test_equipment_component.off_hand = test_shield
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.set_skill_rank(SkillNames.SWORD, 1)
	test_skills_component.set_skill_rank(SkillNames.SHIELD, 1)
	return test_entity

def create_mockchar_7():
	# stats and skills and a sword and shield skill, better at shield than sword, but shield not equipped
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_shield = EquippableFactory.make_shield()
	test_sword = EquippableFactory.make_longsword()
	test_equipment_component.main_hand = test_sword
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.set_skill_rank(SkillNames.SWORD, 14)
	test_skills_component.set_skill_rank(SkillNames.SHIELD, 16)
	return test_entity

def create_mockchar_8():
	# stats and skills and a sword and a shield equipped but no shield skill
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_fighter_component = Fighter()
	test_equipment_component = Equipment()
	test_shield = EquippableFactory.make_shield()
	test_sword = EquippableFactory.make_longsword()
	test_equipment_component.main_hand = test_sword
	test_equipment_component.off_hand = test_shield	
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component, fighter=test_fighter_component)
	test_skills_component.set_skill_rank(SkillNames.SWORD, 14)
	return test_entity

def create_mockchar_9():
	# stats and skills and a bow and no arrows
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_fighter = Fighter()
	test_bow = EquippableFactory.make_shortbow()
	test_equipment_component.main_hand = test_bow
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", fighter=test_fighter, skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	return test_entity

def create_mockchar_10():
	# stats and skills and a bow and arrows
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_fighter = Fighter()
	test_bow = EquippableFactory.make_shortbow()
	test_arrows = EquippableFactory.make_arrows(1, 1, 10)
	test_equipment_component.main_hand = test_bow
	test_equipment_component.ammunition = test_arrows
	test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", fighter=test_fighter, skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	return test_entity

def create_mockchar_11():
	# stats and skills and a sword and shield skill and shield equipped, better at sword than shield
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_level_component = Level()
	test_fighter_component = Fighter()
	test_equipment_component = Equipment()
	test_shield = EquippableFactory.make_shield()
	test_sword = EquippableFactory.make_longsword()
	test_equipment_component.main_hand = test_sword
	test_equipment_component.off_hand = test_shield	
	test_stats_component = Stats(Strength=14, Precision=11, Agility=14, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, level=test_level_component, stats=test_stats_component, defender=test_defender_component, fighter=test_fighter_component)	
	test_skills_component.set_skill_rank(SkillNames.SWORD, 1)
	test_skills_component.set_skill_rank(SkillNames.SHIELD, 1)
	return test_entity

def create_mockchar_12():
	# no weapons, unarmed weapon skill
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_stats_component = Stats(Strength=14, Precision=11, Agility=13	, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component)
	test_skills_component.set_skill_rank(SkillNames.UNARMED, 1)
	test_skills_component.set_skill_rank(SkillNames.SHIELD, 1)
	return test_entity