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
from components.equippable import Equippable, EquippableFactory, make_dropped_missile
from components.skills import Skills
from components.stats import Stats
from components.defender import Defender
from components.meleeweapon import MeleeWeapon
from components.item import Item
from components.name import Name
from components.identified import Identified
from components.effects import Effects
from damage_types import DamageTypes
from loader_functions.constants import get_basic_damage, WeaponTypes, get_constants
from loader_functions.initialize_new_game import get_game_variables, assign_potion_descriptions
from loader_functions.data_loaders import save_game, load_game
from systems.attack import weapon_skill_lookup, get_weapon_skill_for_attack
from systems.effects_manager import add_effect
from systems.name_system import get_display_name
from components.inventory import Inventory
from item_functions import heal
from item_factory import make_healing_potion, make_lightning_scroll, make_fireball_scroll, make_confusion_scroll, make_fireball_book, make_heal_book
import monsters
import mocks
from menus import menu, build_text_menu
import menu_options
import engine

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
		test_item_entity = EquippableFactory.make_sword()
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
		test_skillset.set_skill_rank("sword", 1)
		self.assertEqual(test_skillset.skills["sword"], 1)

	def test_can_update_sword_skill(self):
		test_skillset = Skills()
		test_skillset.set_skill_rank("sword", 1)
		test_skillset.set_skill_rank("sword", 3)
		self.assertEqual(test_skillset.skills["sword"], 3)

	def test_can_get_skill(self):
		test_skillset = Skills()
		test_stats = Stats()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats, skills=test_skillset)
		test_skillset.set_skill_rank("sword", 1)
		skill_test = test_skillset.get_skill_check("sword")
		self.assertEqual(skill_test, 10)
	
	def test_can_get_default(self):
		test_skillset = Skills()
		test_stats = Stats()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats, skills=test_skillset)
		skill_test = test_skillset.get_skill_check("sword")
		self.assertEqual(skill_test, 6)

class MapTests(unittest.TestCase):
	def test_can_make_map(self):
		test_map = maps.GameMap(80, 45)
		self.assertEqual(test_map.width, 80)
		self.assertEqual(test_map.height, 45)
		self.assertEqual(len(test_map.tiles), 80)
		self.assertEqual(len(test_map.tiles[0]), 45)

class StatsTests(unittest.TestCase):
	def test_can_create_entity_with_stats(self):
		test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats_component)
		self.assertEqual(test_entity.stats, test_stats_component)

	def test_can_calculate_hp(self):
		test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats_component)
		self.assertEqual(test_entity.stats.max_hp, 19)
		self.assertEqual(test_entity.stats.hp, 19)


class DamageTests(unittest.TestCase):
	def test_can_load_damage_dictionaries(self):
		swing_damage, thrust_damage = get_basic_damage()
		self.assertNotEqual(len(swing_damage), 0)
		self.assertNotEqual(len(thrust_damage), 0)

	def test_can_calculate_swing_damage(self):
		test_stats_component = Stats(Strength=10, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
		test_fighter_component = Fighter(xp=10)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats_component, fighter=test_fighter_component)
		dice, modifier = test_fighter_component.get_basic_swing_damage()
		self.assertEqual(dice, 1)
		self.assertEqual(modifier, 0)

	def test_can_calculate_thrust_damage(self):
		test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
		test_fighter_component = Fighter(xp=10)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats_component, fighter=test_fighter_component)
		dice, modifier = test_fighter_component.get_basic_thrust_damage()
		self.assertEqual(dice, 1)
		self.assertEqual(modifier, -2)

class AttackTests(unittest.TestCase):
	def test_can_lookup_weapon_skill(self):
		test_weapon = EquippableFactory.make_sword()
		self.assertEqual(weapon_skill_lookup(test_weapon.melee_weapon), "sword")

	def test_can_lookup_correct_weapon_skill(self):
		test_char = mocks.create_mockchar_3()
		weapon = test_char.equipment.main_hand.melee_weapon
		skill_num = get_weapon_skill_for_attack(test_char, weapon)
		self.assertEqual(skill_num, 12)


class DefenderTests(unittest.TestCase):
	def test_can_create_defender(self):
		test_defender_component = Defender()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", defender=test_defender_component)
		self.assertEqual(test_entity.defender, test_defender_component)

	def test_can_get_correct_parry(self):
		test_char = mocks.create_mockchar_3()
		self.assertEqual(test_char.defender.get_parry(), 6)

	def test_can_get_correct_block(self):
		test_char = mocks.create_mockchar_5()
		self.assertEqual(test_char.defender.get_block(), 6)

	def test_can_get_correct_evade(self):
		test_char = mocks.create_mockchar_2()
		self.assertEqual(test_char.defender.get_evade(), 5)

	def test_defender_can_provide_a_defense(self):
		test_char = mocks.create_mockchar_2()
		defense_num = test_char.defender.get_best_melee_defense()
		self.assertNotEqual(defense_num, 0)

	def test_defender_can_choose_best_melee_defense_without_shield(self):
		test_char = mocks.create_mockchar_3()
		results = test_char.defender.get_best_melee_defense()
		self.assertEqual(results[0], "parry")
		self.assertEqual(results[1], 6)

	#def test_defender_can_choose_best_melee_defense_with_shield_and_low_shield_skill(self):
	#	test_char = mocks.create_mockchar_5()
	#	results = test_char.defender.get_best_melee_defense()
	#	self.assertEqual(results[0], "parry")
	#	self.assertEqual(results[1], 6)		

	def test_defender_can_choose_best_melee_defense_with_shield_and_high_shield_skill(self):
		test_char = mocks.create_mockchar_6()
		results = test_char.defender.get_best_melee_defense()
		self.assertEqual(test_char.skills.get_skill_check("shield"), 12)
		self.assertEqual(results[0], "block")
		self.assertEqual(results[1], 6)

	def test_defender_can_choose_best_missile_defense(self):
		test_char = mocks.create_mockchar_1()
		results = test_char.defender.get_best_missile_defense()
		self.assertEqual(results[0], "evade")
		self.assertEqual(results[1], 5)

	def test_defender_can_choose_best_missile_defense_but_not_a_parry(self):
		test_char = mocks.create_mockchar_5()
		results = test_char.defender.get_best_missile_defense()
		self.assertNotEqual(results[0], "parry")

	def test_defender_can_choose_best_missile_defense_with_shield(self):
		test_char = mocks.create_mockchar_5()
		results = test_char.defender.get_best_missile_defense()
		self.assertEqual(results[0], "block")
		self.assertEqual(results[1], 6)


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
		self.assertEqual(len(entities), 2)

class DroppedMissileTests(unittest.TestCase):
	def test_can_drop_missile(self):
		test_monster = monsters.makeKobold(1, 1)
		entities = []
		entities.append(make_dropped_missile("Arrows", (1,1)))
		self.assertEqual(len(entities), 1)

	def test_can_drop_missile_at_correct_location(self):
		test_monster = monsters.makeKobold(1, 1)
		entities = []
		entities.append(make_dropped_missile("Arrows", (1,1)))
		self.assertEqual(entities[0].x, 1)
		self.assertEqual(entities[0].y, 1)
		self.assertEqual(entities[0].name.true_name, "Arrows")

class MissileWeaponTests(unittest.TestCase):
	def test_can_equip_missile_weapon(self):
		test_char = mocks.create_mockchar_1()
		test_bow = EquippableFactory.make_bow()
		test_char.equipment.toggle_equip(test_bow)
		self.assertEqual(test_char.equipment.main_hand, test_bow)
		self.assertNotEqual(test_char.equipment.main_hand.missile_weapon.missile_damage, None)

	def test_can_load_missile_weapon(self):
		test_char = mocks.create_mockchar_10()
		test_char.fighter.load_missile_weapon()
		self.assertEqual(test_char.equipment.main_hand.missile_weapon.loaded, True)

	def test_cannot_load_missile_weapon_without_ammunition(self):
		test_char = mocks.create_mockchar_9()
		results = test_char.fighter.load_missile_weapon()
		self.assertEqual(results[0].get("loaded"), None)

class MeleeWeaponTests(unittest.TestCase):
	def test_can_create_melee_weapon_component(self):
		test_component = MeleeWeapon(WeaponTypes.AXE, "swing", 1, DamageTypes.CRUSHING)
		self.assertEqual(test_component.weapon_type, WeaponTypes.AXE)

	def test_has_melee_weapon(self):
		test_char = mocks.create_mockchar_5()
		self.assertEqual(test_char.equipment.has_melee_weapon(), True)
	# TODO: more of these tests

class NameTests(unittest.TestCase):
	def test_can_make_name_with_display(self):
		test_name = Name("foo")
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, name=test_name)
		self.assertEqual(test_name.true_name, "foo")

	def test_can_make_name_with_true_name(self):
		test_name = Name(true_name="bar")
		self.assertEqual(test_name.true_name, "bar")

	def test_can_make_entity_with_names(self):
		test_name_component = Name(true_name="true")
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, name=test_name_component)
		self.assertEqual(test_entity.name.true_name, "true")

#class ItemTests(unittest.TestCase):
#	def test_can_create_item(self):
#		test_item_component = Item(use_function=None, targeting=False, targeting_message=None)
#		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Test", item=test_item_component)
#		self.assertEqual(test_item_component, test_entity.item)

#	def test_can_create_healing_potion(self):
#		test_item = ItemFactory.makeHealingPotion()
#		self.assertEqual(test_item.name, "Healing Potion")

class GetGameVariablesTests(unittest.TestCase):
	def test_can_create_player(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertEqual(player.name.true_name, "Player")

	def test_can_create_entities(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertEqual(isinstance(entities, list), True)

	def test_can_create_game_map(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertNotEqual(game_map, None)

	def test_can_create_message_log(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertNotEqual(message_log, None)	

	def test_can_create_game_state(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertNotEqual(game_state, None)

	def test_can_create_dlevels(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertNotEqual(dlevels, None)

#class MenuTests(unittest.TestCase):
#	def can_create_main_menu(self):
#		constants = get_constants()
#		options = build_text_menu(['Play a new game', 'Continue a game', 'Quit'])
#		con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
##		main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])

class ItemNamesTests(unittest.TestCase):
	def test_player_has_lists_of_identified_items(self):
		dummy_links = {}
		identified_component = Identified(dummy_links)
		self.assertTrue(isinstance(identified_component.identified_potions, list), True)
		self.assertTrue(isinstance(identified_component.identified_scrolls, list), True)
		self.assertTrue(isinstance(identified_component.potion_links, dict), True)

	def test_game_has_list_of_potion_names(self):
		constants = get_constants()
		self.assertNotEqual(len(constants['potion_descriptions']), 0)

	def test_game_has_list_of_potion_types(self):
		constants = get_constants()
		self.assertNotEqual(len(constants['potion_types']), 0)

	def test_same_number_of_potion_names_and_types(self):
		constants = get_constants()
		self.assertEqual(len(constants['potion_descriptions']), len(constants['potion_types']))

	def test_can_assign_a_potion_name_to_a_type(self):
		constants = get_constants()
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		self.assertNotEqual(len(potion_description_links), 0)

	def test_player_has_potion_links(self):
		constants = get_constants()
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		test_identified_component = Identified(potion_description_links)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, identified=test_identified_component)
		self.assertEqual(isinstance(test_entity.identified.potion_links, dict), True)

	def test_identified_potion_has_correct_display_name(self):
		constants = get_constants()
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		test_identified_component = Identified(potion_description_links)
		test_identified_component.identified_potions.append("Healing Potion")
		test_player = entity.Entity(1, 1, 'A', libtcod.white, identified=test_identified_component)
		test_potion = make_healing_potion()
		self.assertEqual(test_potion.name.true_name, "Healing Potion")
		self.assertTrue("Healing Potion" in test_player.identified.identified_potions)
		self.assertEqual(get_display_name(test_player, test_potion), "Healing Potion")

	def test_unidentified_potion_has_correct_display_name(self):
		constants = get_constants()
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		test_identified_component = Identified(potion_description_links)
		test_player = entity.Entity(1, 1, 'A', libtcod.white, identified=test_identified_component)
		test_potion = make_healing_potion()
		self.assertEqual(test_potion.name.true_name, "Healing Potion")
		self.assertEqual(get_display_name(test_player, test_potion), potion_description_links[test_potion.name.true_name])

class BasicGameTests(unittest.TestCase):
	def test_can_create_new_game(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants, start_equipped=True)
		self.assertEqual(isinstance(entities, list), True)

	def test_can_save_game(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants, start_equipped=True)
		self.assertEqual(save_game(player, entities, game_map, message_log, game_state, dlevels), True)

	def test_can_load_game(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants, start_equipped=True)
		save_game(player, entities, game_map, message_log, game_state, dlevels)
		player, entities, game_map, message_log, game_state, dlevels = load_game()
		self.assertEqual(isinstance(entities, list), True)		

class EffectsTests(unittest.TestCase):
	def test_can_create_effects_component(self):
		effects_component = Effects()
		self.assertEqual(isinstance(effects_component.effect_list, list), True)

	def test_can_add_effects_component_to_entity(self):
		effects_component = Effects()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, effects=effects_component)
		self.assertEqual(isinstance(test_entity.effects.effect_list, list), True)

	def test_effects_manager_can_add_effect(self):
		effects_component = Effects()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, effects=effects_component)
		test_effect = {'name': "Poison", 'turns_left': 5, 'damage_per_turn': 3}
		self.assertEqual(add_effect(test_effect, test_entity), True)

class UseTests(unittest.TestCase):
	def test_can_use_healing_potion(self):
		test_potion = make_healing_potion()
		test_inventory = Inventory(10)
		test_player_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", inventory=test_inventory)
		results = test_inventory.use(test_potion)
		self.assertEqual(len(results), 1)

	def test_can_identify_a_potion(self):
		test_char = mocks.create_mockchar_1()
		self.assertEqual(len(test_char.identified.identified_potions), 0)
		test_potion = make_healing_potion()
		results = test_char.inventory.use(test_potion)
		self.assertEqual(len(test_char.identified.identified_potions), 1)


if __name__ == "__main__":
	unittest.main()
