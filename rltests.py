import unittest
import map_objects.game_map as maps
import engine
import map_objects.tile
import entity
import tcod as libtcod
from equipment_slots import EquipmentSlots
import map_objects.rectangle as rectangle
from components.fighter import Fighter
from components.caster import Caster
from components.equipment import Equipment
from components.equippable import Equippable, EquippableFactory
from components.skills import Skills
from components.stats import Stats
from components.defender import Defender
from components.meleeweapon import MeleeWeapon
from damage_types import DamageTypes
from loader_functions.constants import get_basic_damage, WeaponTypes
from systems.attack import weapon_skill_lookup, get_weapon_skill_for_attack
from components.inventory import Inventory
import monsters
import mocks

class EntityTests(unittest.TestCase):
	def test_can_make_entity(self):
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player")
		self.assertEqual(test_entity.x, 1)

	def test_can_make_entity_with_fighter(self):
		test_fighter = Fighter(xp=10)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", fighter=test_fighter)
		self.assertEqual(test_entity.fighter, test_fighter)

	def test_can_make_entity_with_caster(self):
		test_caster = Caster(spells=[], max_mana=20)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster)
		self.assertEqual(test_entity.caster, test_caster)
		self.assertEqual(test_entity.caster.mana, 20)
		self.assertEqual(test_entity.caster.max_mana, 20)

	def test_can_make_entity_with_caster_who_knows_spells(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster)
		test_caster.learnFireballSpell()
		self.assertEqual(test_caster.spells[0].name, "Fireball")

class SpellTests(unittest.TestCase):
	def test_can_learn_heal(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster)
		test_caster.learnHealSpell()
		self.assertEqual(test_caster.spells[0].name, "Heal")

	def test_can_learn_multiple_spells(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster)
		test_caster.learnHealSpell()
		test_caster.learnFireballSpell()
		self.assertEqual(test_caster.spells[0].name, "Heal")
		self.assertEqual(test_caster.spells[1].name, "Fireball")		

class EquipmentTests(unittest.TestCase):
	def test_can_equip_main_hand(self):
		test_equipment = Equipment()
		test_player_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", equipment=test_equipment)
		test_item_entity = EquippableFactory.makeBroadSword()
		test_equipment.toggle_equip(test_item_entity)
		self.assertEqual(test_player_entity.equipment.main_hand.equippable, test_item_entity.equippable)

	def test_can_create_equipment_component(self):
		test_equipment = Equipment()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", equipment=test_equipment)
		self.assertEqual(test_entity.equipment.main_hand, None)
		self.assertEqual(test_entity.equipment.off_hand, None)
		self.assertEqual(test_entity.equipment.body, None)
		self.assertEqual(test_entity.equipment.ammunition, None)

class SkillsTests(unittest.TestCase):
	def test_can_create_and_link_skills_component(self):
		test_skillset = Skills()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", skills=test_skillset)
		self.assertEqual(test_entity.skills, test_skillset)
	 
	def test_can_create_sword_skill(self):
		test_skillset = Skills()
		test_skillset.setSkill("sword", 15)
		self.assertEqual(test_skillset.skills["sword"], 15)

	def test_can_update_sword_skill(self):
		test_skillset = Skills()
		test_skillset.setSkill("sword", 15)
		test_skillset.setSkill("sword", 18)
		self.assertEqual(test_skillset.skills["sword"], 18)

	def test_can_get_skill(self):
		test_skillset = Skills()
		test_skillset.setSkill("sword", 15)
		foo = test_skillset.getSkill("sword")
		self.assertEqual(foo, 15)
	
	# TODO: this uses the crappy default, fix it later
	def test_can_get_skill_default(self):
		test_skillset = Skills()
		foo = test_skillset.getSkill("sword")
		self.assertEqual(foo, 8)	


class MapTests(unittest.TestCase):
	def test_can_make_map(self):
		test_map = maps.GameMap(80, 45)
		self.assertEqual(test_map.width, 80)
		self.assertEqual(test_map.height, 45)
		self.assertEqual(len(test_map.tiles), 80)
		self.assertEqual(len(test_map.tiles[0]), 45)

class StatsTests(unittest.TestCase):
	def test_can_create_entity_with_stats(self):
		test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats_component)
		self.assertEqual(test_entity.stats, test_stats_component)

	def test_can_calculate_hp(self):
		test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats_component)
		self.assertEqual(test_entity.stats.max_hp, 10)
		self.assertEqual(test_entity.stats.hp, 10)


class DamageTests(unittest.TestCase):
	def test_can_load_damage_dictionaries(self):
		swing_damage, thrust_damage = get_basic_damage()
		self.assertNotEqual(len(swing_damage), 0)
		self.assertNotEqual(len(thrust_damage), 0)

	def test_can_calculate_swing_damage(self):
		test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
		test_fighter_component = Fighter(xp=10)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats_component, fighter=test_fighter_component)
		dice, modifier = test_fighter_component.get_basic_swing_damage()
		self.assertEqual(dice, 1)
		self.assertEqual(modifier, 0)

	def test_can_calculate_thrust_damage(self):
		test_stats_component = Stats(ST=10, DX=10, IQ=10, HT=10)
		test_fighter_component = Fighter(xp=10)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats_component, fighter=test_fighter_component)
		dice, modifier = test_fighter_component.get_basic_thrust_damage()
		self.assertEqual(dice, 1)
		self.assertEqual(modifier, -2)

class AttackTests(unittest.TestCase):
	def test_can_lookup_weapon_skill(self):
		test_weapon = EquippableFactory.makeBroadSword()
		self.assertEqual(weapon_skill_lookup(test_weapon.melee_weapon), "sword")

	def test_can_lookup_correct_weapon_skill(self):
		test_char = mocks.create_mockchar_3()
		weapon = test_char.equipment.main_hand.melee_weapon
		skill_num = get_weapon_skill_for_attack(test_char, weapon)
		self.assertEqual(skill_num, 14)


class DefenderTests(unittest.TestCase):
	def test_can_create_defender(self):
		test_defender_component = Defender()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", defender=test_defender_component)
		self.assertEqual(test_entity.defender, test_defender_component)

	def test_can_get_correct_parry(self):
		test_char = mocks.create_mockchar_3()
		test_char_pd = test_char.equipment.PD_bonus
		self.assertEqual(test_char.defender.get_parry(), (7 + test_char_pd))

	def test_can_get_correct_block(self):
		test_char = mocks.create_mockchar_5()
		test_char_pd = test_char.equipment.PD_bonus
		self.assertEqual(test_char.defender.get_block(), (6 + test_char_pd))

	def test_can_get_correct_dodge(self):
		test_char = mocks.create_mockchar_2()
		test_char_pd = test_char.equipment.PD_bonus
		self.assertEqual(test_char.defender.get_dodge(), (5 + test_char_pd))

	def test_defender_can_provide_a_defense(self):
		test_char = mocks.create_mockchar_2()
		defense_num = test_char.defender.get_best_melee_defense()
		self.assertNotEqual(defense_num, 0)

	def test_defender_can_choose_best_melee_defense_without_shield(self):
		test_char = mocks.create_mockchar_3()
		test_char_pd = test_char.equipment.PD_bonus
		results = test_char.defender.get_best_melee_defense()
		self.assertEqual(results[0], "parry")
		self.assertEqual(results[1], (7 + test_char_pd))

	def test_defender_can_choose_best_melee_defense_with_shield_and_low_shield_skill(self):
		test_char = mocks.create_mockchar_5()
		test_char_pd = test_char.equipment.PD_bonus
		results = test_char.defender.get_best_melee_defense()
		self.assertEqual(results[0], "parry")
		self.assertEqual(results[1], (7 + test_char_pd))		

	def test_defender_can_choose_best_melee_defense_with_shield_and_high_shield_skill(self):
		test_char = mocks.create_mockchar_6()
		test_char_pd = test_char.equipment.PD_bonus
		results = test_char.defender.get_best_melee_defense()
		self.assertEqual(results[0], "block")
		self.assertEqual(results[1], (8 + test_char_pd))

	def test_defender_can_choose_best_missile_defense(self):
		test_char = mocks.create_mockchar_1()
		test_char_pd = test_char.equipment.PD_bonus
		results = test_char.defender.get_best_missile_defense()
		self.assertEqual(results[0], "dodge")
		self.assertEqual(results[1], (5 + test_char_pd))

	def test_defender_can_choose_best_missile_defense_but_not_a_parry(self):
		test_char = mocks.create_mockchar_5()
		test_char_pd = test_char.equipment.PD_bonus
		results = test_char.defender.get_best_missile_defense()
		self.assertNotEqual(results[0], "parry")

	def test_defender_can_choose_best_missile_defense_with_shield(self):
		test_char = mocks.create_mockchar_5()
		test_char_pd = test_char.equipment.PD_bonus
		results = test_char.defender.get_best_missile_defense()
		self.assertEqual(results[0], "block")
		self.assertEqual(results[1], (6 + test_char_pd)) 

class DeathDropTests(unittest.TestCase):
	def test_monster_has_items(self):
		test_monster = monsters.makeKobold(1, 1)
		self.assertNotEqual(len(test_monster.inventory.items), 0)

	def test_kobold_drops_all_items(self):
		test_monster = monsters.makeKobold(1, 1)
		entities = []
		entities = test_monster.inventory.drop_on_death(entities, test_monster)
		self.assertEqual(len(entities), 3)

	def test_orc_drops_all_items(self):
		test_monster = monsters.makeOrc(1, 1)
		entities = []
		entities = test_monster.inventory.drop_on_death(entities, test_monster)
		for entity in entities:
			print(entity.name)
		self.assertEqual(len(entities), 2)

	def test_monster_drops_one_item(self):
		pass

class DroppedMissileTests(unittest.TestCase):
	def test_can_drop_missile(self):
		pass

	def test_can_drop_missile_at_correct_location(self):
		pass
	

class MeleeWeaponTests(unittest.TestCase):
	def test_can_create_melee_weapon_component(self):
		test_component = MeleeWeapon(WeaponTypes.AXE, "swing", 1, DamageTypes.CRUSHING)
		self.assertEqual(test_component.weapon_type, WeaponTypes.AXE)	

if __name__ == "__main__":
	unittest.main()
