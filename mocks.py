import tcod as libtcod
from components.fighter import Fighter
from components.caster import Caster
from components.equipment import Equipment
from components.equippable import Equippable, EquippableFactory
from components.skills import Skills
from components.stats import Stats
from components.defender import Defender
from entity import Entity

def create_mockchar_1():
	# basic stats, no skills or equipment
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	return test_entity

def create_mockchar_2():
	# basic stats and skills, no equipment
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.setSkill("sword", 14)
	test_skills_component.setSkill("shield", 12)
	return test_entity

def create_mockchar_3():
	# stats and skills and a sword, no shield skill or equipped
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	equippable_component = EquippableFactory.makeBroadSword()
	test_item_entity = Entity(1, 1, 'B', libtcod.white, "Sword", equippable=equippable_component)
	test_equipment_component.main_hand = test_item_entity	
	test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.setSkill("sword", 14)
	return test_entity

def create_mockchar_4():
	# stats and skills and a sword, shield skill, has a shield but no shield equipped
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	equippable_component = EquippableFactory.makeShield()
	test_item_entity = Entity(1, 1, 'B', libtcod.white, "Shield", equippable=equippable_component)
	equippable_component2 = EquippableFactory.makeBroadSword()
	test_item_entity2 = Entity(1, 1, 'B', libtcod.white, "Sword", equippable=equippable_component2)
	test_equipment_component.main_hand = test_item_entity2
	#test_equipment_component.off_hand = test_item_entity	
	test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.setSkill("sword", 14)
	return test_entity

def create_mockchar_5():
	# stats and skills and a sword and shield skill and shield equipped, better at sword than shield
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	equippable_component = EquippableFactory.makeShield()
	test_item_entity = Entity(1, 1, 'B', libtcod.white, "Shield", equippable=equippable_component)
	equippable_component2 = EquippableFactory.makeBroadSword()
	test_item_entity2 = Entity(1, 1, 'B', libtcod.white, "Sword", equippable=equippable_component2)
	test_equipment_component.main_hand = test_item_entity2
	test_equipment_component.off_hand = test_item_entity	
	test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.setSkill("sword", 14)
	test_skills_component.setSkill("shield", 12)
	return test_entity	

def create_mockchar_6():
	# stats and skills and a sword and shield skill, better at shield than sword, and shield equipped
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	equippable_component = EquippableFactory.makeShield()
	test_item_entity = Entity(1, 1, 'B', libtcod.white, "Shield", equippable=equippable_component)
	equippable_component2 = EquippableFactory.makeBroadSword()
	test_item_entity2 = Entity(1, 1, 'B', libtcod.white, "Sword", equippable=equippable_component2)
	test_equipment_component.main_hand = test_item_entity2
	test_equipment_component.off_hand = test_item_entity	
	test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.setSkill("sword", 14)
	test_skills_component.setSkill("shield", 16)
	return test_entity

def create_mockchar_7():
	# stats and skills and a sword and shield skill, better at shield than sword, but shield not equipped
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	equippable_component = EquippableFactory.makeShield()
	test_item_entity = Entity(1, 1, 'B', libtcod.white, "Shield", equippable=equippable_component)
	equippable_component2 = EquippableFactory.makeBroadSword()
	test_item_entity2 = Entity(1, 1, 'B', libtcod.white, "Sword", equippable=equippable_component2)
	test_equipment_component.main_hand = test_item_entity2
	test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.setSkill("sword", 14)
	test_skills_component.setSkill("shield", 16)
	return test_entity

def create_mockchar_8():
	# stats and skills and a sword and a shield equipped but no shield skill
	test_defender_component = Defender()
	test_skills_component = Skills()
	test_equipment_component = Equipment()
	equippable_component = EquippableFactory.makeShield()
	test_item_entity = Entity(1, 1, 'B', libtcod.white, "Shield", equippable=equippable_component)
	equippable_component2 = EquippableFactory.makeBroadSword()
	test_item_entity2 = Entity(1, 1, 'B', libtcod.white, "Sword", equippable=equippable_component2)
	test_equipment_component.main_hand = test_item_entity2
	test_equipment_component.off_hand = test_item_entity	
	test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
	test_entity = Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skills_component, equipment=test_equipment_component, stats=test_stats_component, defender=test_defender_component)	
	test_skills_component.setSkill("sword", 14)
	return test_entity