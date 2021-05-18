import unittest
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
from components.effects import Effect
from components.performer import Performer
from components.consumable import ConsumableTypes, get_carried_potions
from components.inventory import Inventory
from damage_types import DamageTypes
from death_functions import kill_monster
from loader_functions.constants import WeaponTypes, WeaponCategories, get_constants, AmmunitionTypes
from loader_functions.initialize_new_game import get_game_variables, assign_potion_descriptions, assign_scroll_descriptions, populate_dlevels
from loader_functions.data_loaders import save_game, load_game
from systems.attack import weapon_skill_lookup, get_weapon_skill_for_attack, get_hit_modifier_from_status_effects
from systems.effects_manager import add_effect, tick_down_effects, process_damage_over_time, EffectNames
from systems.name_system import get_display_name
from systems.damage import get_physical_damage_modifier_from_status_effects, get_physical_damage_modifier_from_equipment, apply_physical_damage_modifiers, get_damage_string, get_current_missile_damage, get_current_melee_damage
from systems.attack import get_hit_modifier_from_status_effects, get_hit_modifier_from_equipment, attack
from systems.spell_system import learn_spell, cast, get_spell_target
from systems.skill_manager import SkillNames, get_intellect, get_willpower
from systems.move_system import distance_to
from systems.pickup_system import pickup_item
from systems.feat_system import get_targetable_entities_in_range
from magic_functions import heal, learn_spell_from_book, make_bless_spell
from fov_functions import initialize_fov
from render_functions import get_names_under_mouse
from item_factory import make_healing_potion, make_fireball_scroll, make_confusion_scroll, make_fireball_book, make_heal_book, make_bless_book, make_poison_potion, make_confusion_potion
from components.equippable import EquippableFactory
import monsters
import mocks
from menus import menu
import menu_options
from attack_types import AttackTypes
from menus import get_equipped_items

class EntityTests(unittest.TestCase):
	def test_can_make_entity(self):
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player")
		self.assertEqual(test_entity.x, 1)

	def test_can_make_entity_with_fighter(self):
		test_fighter = Fighter(xp_reward=10)
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
		learn_spell(test_entity, 'fireball')
		self.assertEqual(test_caster.spells[0].name, "Fireball")

class SpellTests(unittest.TestCase):
	def test_can_learn_heal(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster)
		learn_spell(test_entity, 'heal')
		self.assertEqual(test_caster.spells[0].name, "Heal")

	def test_can_learn_bless(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster)
		learn_spell(test_entity, 'bless')
		self.assertEqual(test_caster.spells[0].name, "Bless")

	def test_can_learn_bless_from_book(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster)
		learn_spell_from_book(test_entity, spell_name='bless')
		self.assertEqual(test_caster.spells[0].name, "Bless")

	def test_can_learn_multiple_spells(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster)
		learn_spell(test_entity, 'heal')
		learn_spell(test_entity, 'fireball')
		self.assertEqual(test_caster.spells[0].name, "Heal")
		self.assertEqual(test_caster.spells[1].name, "Fireball")

	def test_can_cast_bless_spell_with_high_skill(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_fighter = Fighter(xp_reward=100)
		test_stats = Stats()
		test_skills = Skills()
		test_skills.set_skill_rank(SkillNames.HOLY, 8)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster, fighter=test_fighter, skills=test_skills, stats=test_stats)
		entities = []
		entities.append(test_entity)
		spell = make_bless_spell()
		results = cast(test_entity, spell, target_x=1, target_y=1, entities=entities)
		self.assertTrue(len(results), 1)
		self.assertEqual(len(test_entity.fighter.effect_list), 1)
		self.assertEqual(test_entity.fighter.effect_list[0].name, EffectNames.BLESS)
		self.assertEqual(test_entity.fighter.effect_list[0].turns_left, 25)
		self.assertEqual(get_hit_modifier_from_status_effects(test_entity), 1)
		self.assertEqual(get_physical_damage_modifier_from_status_effects(test_entity), 1)

	def test_cannot_cast_bless_spell_with_no_skill(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_fighter = Fighter(xp_reward=100)
		test_stats = Stats(Strength=1, Precision=1, Agility=1, Intellect=1, Willpower=1, Stamina=1, Endurance=1)
		test_skills = Skills()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster, fighter=test_fighter, skills=test_skills, stats=test_stats)
		entities = []
		entities.append(test_entity)
		spell = make_bless_spell()
		results = cast(test_entity, spell, target_x=1, target_y=1, entities=entities)
		self.assertTrue(len(results), 1)
		self.assertEqual(len(test_entity.fighter.effect_list), 0)

	def test_can_get_spell_target(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		fov_map = initialize_fov(game_map)
		test_monster = mocks.create_mockchar_11()
		test_monster.x, test_monster.y = 2, 2
		entities = [player, test_monster]
		self.assertEqual(get_spell_target(player, 2, 2, entities, fov_map), test_monster)

	def test_cannot_get_spell_target_out_of_range(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		fov_map = initialize_fov(game_map)
		test_monster = mocks.create_mockchar_11()
		test_monster.x, test_monster.y = 10, 10
		entities = [player, test_monster]
		self.assertEqual(get_spell_target(player, 2, 2, entities, fov_map), None)

class EquipmentTests(unittest.TestCase):
	def test_can_equip_main_hand(self):
		test_equipment = Equipment()
		test_player_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", equipment=test_equipment)
		test_item_entity = EquippableFactory.make_longsword()
		test_equipment.toggle_equip(test_item_entity)
		self.assertEqual(test_player_entity.equipment.main_hand.equippable, test_item_entity.equippable)

	def test_can_create_equipment_component(self):
		test_equipment = Equipment()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", equipment=test_equipment)
		self.assertEqual(test_entity.equipment.main_hand, None)
		self.assertEqual(test_entity.equipment.off_hand, None)
		self.assertEqual(test_entity.equipment.body, None)
		self.assertEqual(test_entity.equipment.ammunition, None)

	def test_can_get_equipped_items(self):
		test_equipment = Equipment()
		test_char = entity.Entity(1, 1, 'A', libtcod.white, "Player", equipment=test_equipment)
		self.assertEqual(len(get_equipped_items(test_char)), 4)

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
		test_skillset.set_skill_rank(SkillNames.SWORD, 1)
		skill_test = test_skillset.get_skill_check(SkillNames.SWORD)
		self.assertEqual(skill_test, 10)
	
	def test_can_get_default(self):
		test_skillset = Skills()
		test_stats = Stats()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats, skills=test_skillset)
		skill_test = test_skillset.get_skill_check(SkillNames.SWORD)
		self.assertEqual(skill_test, 6)

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

	def test_can_calculate_physical_damage_modifier_from_equipment(self):
		test_equipment = Equipment()
		padded_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=1, physical_damage_modifier=2)
		padded_armor_name = Name("Padded Armor")
		padded_armor_entity = entity.Entity(1, 1, ')', libtcod.purple, equippable=padded_armor_equippable, name=padded_armor_name)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", equipment=test_equipment)
		test_equipment.body = padded_armor_entity
		self.assertEqual(get_physical_damage_modifier_from_equipment(test_entity), 2)

	def test_can_calculate_damage_bonus_from_effects(self):
		test_caster = Caster(spells=[], max_mana=50)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", caster=test_caster)
		learn_spell(test_entity, 'bless')

	def test_can_apply_damage_modifiers(self):
		test_equipment = Equipment()
		test_fighter = Fighter(xp_reward=100)
		padded_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=1, physical_damage_modifier=2)
		padded_armor_name = Name("Padded Armor")
		padded_armor_entity = entity.Entity(1, 1, ')', libtcod.purple, equippable=padded_armor_equippable, name=padded_armor_name)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", equipment=test_equipment, fighter=test_fighter)
		test_equipment.body = padded_armor_entity
		modifier = 0
		modifier += apply_physical_damage_modifiers(modifier, test_entity)
		self.assertEqual(modifier, 2)

	def test_can_get_damage_string(self):
		test_stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
		test_fighter_component = Fighter(xp_reward=10)
		test_equipment = Equipment()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", stats=test_stats_component, fighter=test_fighter_component, equipment=test_equipment)
		self.assertTrue("d" in get_damage_string(test_entity))

class AttackTests(unittest.TestCase):
	def test_can_lookup_weapon_skill(self):
		test_weapon = EquippableFactory.make_longsword()
		self.assertEqual(weapon_skill_lookup(test_weapon), SkillNames.SWORD)
		test_weapon2 = EquippableFactory.make_greatsword()
		self.assertEqual(weapon_skill_lookup(test_weapon2), SkillNames.SWORD)

	def test_can_lookup_correct_weapon_skill(self):
		test_char = mocks.create_mockchar_3()
		weapon = test_char.equipment.main_hand
		skill_num = get_weapon_skill_for_attack(test_char)
		self.assertEqual(skill_num, 10)

	def test_can_lookup_unarmed_skill_if_no_weapon(self):
		test_char = mocks.create_mockchar_12()
		skill_num = get_weapon_skill_for_attack(test_char)
		self.assertEqual(skill_num, 12)

	def test_can_get_equipment_attack_bonus(self):
		test_equipment = Equipment()
		padded_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=1, hit_modifier=2)
		padded_armor_name = Name("Padded Armor")
		padded_armor_entity = entity.Entity(1, 1, ')', libtcod.purple, equippable=padded_armor_equippable, name=padded_armor_name)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", equipment=test_equipment)
		test_equipment.body = padded_armor_entity
		self.assertEqual(get_hit_modifier_from_equipment(test_entity), 2)

	def test_can_perform_melee_attack(self):
		test_char = mocks.create_mockchar_3()
		test_enemy = mocks.create_mockchar_3()
		results = attack(test_char, test_enemy, AttackTypes.MELEE)
		self.assertNotEqual(len(results), 0)

	def test_can_perform_attack_with_feat_bonuses(self):
		#TODO: Make this testable somehow!
		pass

class DefenderTests(unittest.TestCase):
	def test_can_create_defender(self):
		test_defender_component = Defender()
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", defender=test_defender_component)
		self.assertEqual(test_entity.defender, test_defender_component)

	def test_can_get_correct_parry(self):
		test_char = mocks.create_mockchar_3()
		self.assertEqual(test_char.defender.get_parry(), 5)

	def test_can_get_correct_block(self):
		test_char = mocks.create_mockchar_5()
		self.assertEqual(test_char.defender.get_block(), 5)

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
		self.assertEqual(results[1], 5)

	#def test_defender_can_choose_best_melee_defense_with_shield_and_low_shield_skill(self):
	#	test_char = mocks.create_mockchar_5()
	#	results = test_char.defender.get_best_melee_defense()
	#	self.assertEqual(results[0], "parry")
	#	self.assertEqual(results[1], 6)		

	def test_defender_can_choose_best_melee_defense_with_shield_and_high_shield_skill(self):
		test_char = mocks.create_mockchar_6()
		results = test_char.defender.get_best_melee_defense()
		self.assertEqual(test_char.skills.get_skill_check(SkillNames.SHIELD), 10)
		self.assertEqual(results[0], "block")
		self.assertEqual(results[1], 5)

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
		test_char = mocks.create_mockchar_11()
		results = test_char.defender.get_best_missile_defense()
		self.assertEqual(results[0], "block")
		self.assertEqual(results[1], 7)

class DeathTests(unittest.TestCase):
	def test_killing_a_monster_gives_xp(self):
		# TODO: write this test
		test_char = mocks.create_mockchar_11()
		test_monster = monsters.make_orc(1, 1)
		self.assertEqual(test_char.level.current_xp, 0)
		message = message, test_char = kill_monster(test_monster, test_char)
		self.assertGreater(test_char.level.current_xp, 0)

class DeathDropTests(unittest.TestCase):
	def test_monster_has_items(self):
		test_monster = monsters.make_kobold(1, 1)
		self.assertNotEqual(len(test_monster.inventory.items), 0)

	def test_kobold_drops_all_items(self):
		test_monster = monsters.make_kobold(1, 1)
		entities = []
		entities = test_monster.inventory.drop_on_death(entities, test_monster)
		self.assertEqual(len(entities), 3)

	def test_orc_drops_all_items(self):
		test_monster = monsters.make_orc(1, 1)
		entities = []
		entities = test_monster.inventory.drop_on_death(entities, test_monster)
		self.assertEqual(len(entities), 2)

class DroppedMissileTests(unittest.TestCase):
	def test_can_drop_missile(self):
		test_monster = monsters.make_kobold(1, 1)
		entities = []
		entities.append(make_dropped_missile(AmmunitionTypes.ARROWS, (1,1)))
		self.assertEqual(len(entities), 1)

	def test_can_drop_missile_at_correct_location(self):
		test_monster = monsters.make_kobold(1, 1)
		entities = []
		entities.append(make_dropped_missile(AmmunitionTypes.ARROWS, (1,1)))
		self.assertEqual(entities[0].x, 1)
		self.assertEqual(entities[0].y, 1)
		self.assertEqual(entities[0].name.true_name, "Arrow")

class MissileWeaponTests(unittest.TestCase):
	def test_can_create_arrows(self):
		test_arrows = EquippableFactory.make_arrows(1, 1, 10)
		self.assertEqual(test_arrows.item.quantity, 10)

	def test_can_equip_missile_weapon(self):
		test_char = mocks.create_mockchar_1()
		test_bow = EquippableFactory.make_shortbow()
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

	def test_can_get_missile_weapon_damage(self):
		test_char = mocks.create_mockchar_1()
		test_bow = EquippableFactory.make_shortbow()
		test_char.equipment.toggle_equip(test_bow)
		self.assertEqual(get_current_missile_damage(test_char), (1,6,0, DamageTypes.PIERCING))

	def test_can_check_if_has_ammunition(self):
		test_char = mocks.create_mockchar_10()
		self.assertEqual(test_char.equipment.has_ammunition(), True)

	def test_has_ammunition_returns_false_if_no_arrows(self):
		test_char = mocks.create_mockchar_9()
		self.assertEqual(test_char.equipment.has_ammunition(), False)		

class MeleeWeaponTests(unittest.TestCase):
	def test_can_create_melee_weapon_component(self):
		test_component = MeleeWeapon(WeaponTypes.AXE, WeaponCategories.AXE, "swing", 1, DamageTypes.CRUSHING)
		self.assertEqual(test_component.weapon_type, WeaponTypes.AXE)

	def test_has_melee_weapon(self):
		test_char = mocks.create_mockchar_5()
		self.assertEqual(test_char.equipment.has_melee_weapon(), True)
	
	def test_can_get_current_melee_damage(self):
		test_char = mocks.create_mockchar_5()
		self.assertEqual(get_current_melee_damage(test_char), (1,6,0, DamageTypes.SLASHING))	


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

	def test_can_populate_dlevels(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		dlevels = populate_dlevels(entities, game_map, 6)
		self.assertTrue(1 in dlevels.keys())
		self.assertTrue(6 in dlevels.keys())
		self.assertTrue(7 not in dlevels.keys())

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

	def test_game_has_list_of_scroll_names(self):
		constants = get_constants()
		self.assertNotEqual(len(constants['scroll_descriptions']), 0)

	def test_game_has_list_of_potion_types(self):
		constants = get_constants()
		self.assertNotEqual(len(constants['potion_types']), 0)

	def test_game_has_list_of_scroll_types(self):
		constants = get_constants()
		self.assertNotEqual(len(constants['scroll_types']), 0)	

	def test_same_number_of_potion_names_and_types(self):
		constants = get_constants()
		self.assertEqual(len(constants['potion_descriptions']), len(constants['potion_types']))

	def test_same_number_of_scroll_names_and_types(self):
		constants = get_constants()
		self.assertEqual(len(constants['scroll_descriptions']), len(constants['scroll_types']))	

	def test_can_assign_a_potion_name_to_a_type(self):
		constants = get_constants()
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		self.assertNotEqual(len(potion_description_links), 0)

	def test_can_assign_a_scroll_name_to_a_type(self):
		constants = get_constants()
		scroll_description_links = assign_scroll_descriptions(constants['scroll_descriptions'], constants['scroll_types'])
		self.assertNotEqual(len(scroll_description_links), 0)

	def test_player_has_potion_links(self):
		constants = get_constants()
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		test_identified_component = Identified(potion_description_links)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, identified=test_identified_component)
		self.assertEqual(isinstance(test_entity.identified.potion_links, dict), True)

	def test_player_has_scroll_links(self):
		constants = get_constants()
		scroll_description_links = assign_scroll_descriptions(constants['scroll_descriptions'], constants['scroll_types'])
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		test_identified_component = Identified(potion_description_links, scroll_description_links)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, identified=test_identified_component)
		self.assertEqual(isinstance(test_entity.identified.scroll_links, dict), True)

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
		self.assertEqual(test_potion.consumable.consumable_type, ConsumableTypes.POTION)
		self.assertEqual(test_potion.name.true_name, "Healing Potion")
		self.assertEqual(get_display_name(test_player, test_potion), potion_description_links[test_potion.name.true_name])

	def test_identified_scroll_has_correct_display_name(self):
		constants = get_constants()
		scroll_description_links = assign_scroll_descriptions(constants['scroll_descriptions'], constants['scroll_types'])
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		test_identified_component = Identified(potion_description_links, scroll_description_links)
		test_identified_component.identified_scrolls.append("Confusion Scroll")
		test_player = entity.Entity(1, 1, 'A', libtcod.white, identified=test_identified_component)
		test_scroll = make_confusion_scroll()
		self.assertEqual(test_scroll.name.true_name, "Confusion Scroll")
		self.assertTrue("Confusion Scroll" in test_player.identified.identified_scrolls)
		self.assertEqual(get_display_name(test_player, test_scroll), "Confusion Scroll")

	def test_unidentified_scroll_has_correct_display_name(self):
		constants = get_constants()
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		scroll_description_links = assign_scroll_descriptions(constants['scroll_descriptions'], constants['scroll_types'])
		test_identified_component = Identified(potion_description_links, scroll_description_links)
		test_player = entity.Entity(1, 1, 'A', libtcod.white, identified=test_identified_component)
		test_scroll = make_confusion_scroll()
		self.assertEqual(test_scroll.consumable.consumable_type, ConsumableTypes.SCROLL)
		self.assertEqual(test_scroll.name.true_name, "Confusion Scroll")
		self.assertEqual(get_display_name(test_player, test_scroll), scroll_description_links[test_scroll.name.true_name])

	def test_using_an_unidentified_scroll_identifies_it(self):
		constants = get_constants()
		potion_description_links = assign_potion_descriptions(constants['potion_descriptions'], constants['potion_types'])
		scroll_description_links = assign_scroll_descriptions(constants['scroll_descriptions'], constants['scroll_types'])
		test_identified_component = Identified(potion_description_links, scroll_description_links)
		test_inventory = Inventory(10)
		test_player = entity.Entity(1, 1, 'A', libtcod.white, identified=test_identified_component, inventory=test_inventory)
		test_scroll = make_confusion_scroll()
		self.assertEqual(len(test_identified_component.identified_scrolls), 0)
		test_inventory.use(test_scroll)
		self.assertEqual(len(test_identified_component.identified_scrolls), 1)
		#self.assertTrue('onfusion' in test_identified_component.identified_scrolls)

class BasicGameTests(unittest.TestCase):
	def test_can_create_new_game(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertEqual(isinstance(entities, list), True)

	def test_can_save_game(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertEqual(save_game(player, entities, game_map, message_log, game_state, dlevels), True)

	def test_can_load_game(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		save_game(player, entities, game_map, message_log, game_state, dlevels)
		player, entities, game_map, message_log, game_state, dlevels = load_game()
		self.assertEqual(isinstance(entities, list), True)		

	def test_game_starts_with_turn_count(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertEqual(game_state.game_turn, 0)

class CharacterTests(unittest.TestCase):
	def test_can_create_character_with_stats(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertTrue(player.stats)
	def test_can_create_character_with_correct_stats(self):
		constants = get_constants()
		player, entities, game_map, message_log, game_state, dlevels = get_game_variables(constants)
		self.assertTrue(player.stats.Strength, 16)

class EffectsTests(unittest.TestCase):

	def test_effects_manager_can_add_effect(self):
		test_fighter = Fighter(xp_reward=100)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_fighter)
		test_effect = Effect(name=EffectNames.POISON, description="Poisoned", turns_left=5, damage_per_turn=3)
		self.assertEqual(add_effect(test_effect, test_entity), "appended")
		self.assertEqual(len(test_fighter.effect_list), 1)

	def test_effects_stack_properly(self):
		test_fighter = Fighter(xp_reward=100)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_fighter)
		test_effect = Effect(name=EffectNames.POISON, description="Poisoned", turns_left=5, damage_per_turn=3)
		add_effect(test_effect, test_entity)
		test_effect_2 = Effect(name=EffectNames.POISON, description="Poisoned", turns_left=3, damage_per_turn=3)
		self.assertEqual(add_effect(test_effect_2, test_entity), "extended")
		self.assertEqual(test_fighter.effect_list[0].turns_left, 8)

	def test_effects_tick_down(self):
		test_fighter = Fighter(xp_reward=100)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_fighter)
		test_effect = Effect(name=EffectNames.POISON, description="Poisoned", turns_left=5, damage_per_turn=3)
		add_effect(test_effect, test_entity)
		tick_down_effects(test_entity)
		self.assertEqual(test_effect.turns_left, 4)

	def test_effects_disappear_when_done(self):
		test_fighter = Fighter(xp_reward=100)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_fighter)
		test_effect = Effect(name=EffectNames.POISON, description="Poisoned", turns_left=5, damage_per_turn=3)
		add_effect(test_effect, test_entity)
		self.assertEqual(len(test_entity.fighter.effect_list), 1)
		for _ in range(5):
			tick_down_effects(test_entity)
		self.assertEqual(len(test_entity.fighter.effect_list), 0)

	def test_damage_over_time_effects_work(self):
		fighter_component = Fighter(xp_reward=100)
		stats_component = Stats(Strength=9, Precision=11, Agility=12, Intellect=10, Willpower=9, Stamina=10, Endurance=9)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, stats=stats_component, fighter=fighter_component)
		test_effect = Effect(name=EffectNames.POISON, description="Poisoned", turns_left=5, damage_per_turn=3)
		add_effect(test_effect, test_entity)
		process_damage_over_time(test_entity)
		self.assertEqual(test_entity.stats.hp, 16)

	def test_can_calculate_hit_bonus_from_effects(self):
		test_fighter = Fighter(xp_reward=100)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_fighter)
		test_effect = Effect(name=EffectNames.POISON, description="Poisoned", turns_left=5, damage_per_turn=3)
		add_effect(test_effect, test_entity)
		self.assertEqual(get_hit_modifier_from_status_effects(test_entity), 0)
		test_effect_2 = Effect(name=EffectNames.BLESS, description="Blessed", turns_left=5, hit_modifier=3)
		add_effect(test_effect_2, test_entity)
		self.assertEqual(get_hit_modifier_from_status_effects(test_entity), 3)

	def test_can_calculate_damage_bonus_from_effects(self):
		test_fighter = Fighter(xp_reward=100)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_fighter)
		self.assertEqual(get_physical_damage_modifier_from_status_effects(test_entity), 0)
		test_effect = Effect(name=EffectNames.BLESS, description="Blessed", turns_left=5, physical_damage_modifier=3)
		add_effect(test_effect, test_entity)
		self.assertEqual(get_physical_damage_modifier_from_status_effects(test_entity), 3)

	def test_can_apply_a_confuse_effect(self):
		test_player = mocks.create_mockchar_3()
		test_effect = Effect(name=EffectNames.CONFUSION, description="Confused", turns_left=5)
		add_effect(test_effect, test_player)
		self.assertEqual(test_player.fighter.effect_list[0].name, EffectNames.CONFUSION)


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

	def test_can_use_confusion_potion(self):
		test_potion = make_confusion_potion()
		test_inventory = Inventory(10)
		test_inventory.items.append(test_potion)
		test_player_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", inventory=test_inventory)
		test_inventory.use(test_potion)
		#self.assertEqual(results[0].get('consumed'), True)

class MoveTests(unittest.TestCase):
	def test_can_calculate_distance_to(self):
		test_entity_1 = entity.Entity(1, 1, 'A', libtcod.white)
		test_entity_2 = entity.Entity(4, 5, 'A', libtcod.white)
		self.assertEqual(distance_to(test_entity_1, test_entity_2), 5)

class BookTests(unittest.TestCase):
	def test_can_make_and_hold_bless_book(self):
		test_book = make_bless_book()
		test_inventory = Inventory(10)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, inventory=test_inventory)
		test_inventory.add_item(test_book)
		self.assertTrue(len(test_inventory.items) == 1)
		self.assertEqual(test_inventory.items[0].name.true_name, "Bless spellbook")

class PotionMenuTests(unittest.TestCase):
	def test_can_produce_list_of_potions_for_menu(self):
		test_potion = make_healing_potion()
		test_potion2 = make_poison_potion()
		test_inventory = Inventory(10)
		test_inventory.items.append(test_potion)
		test_inventory.items.append(test_potion2)
		test_player = entity.Entity(1, 1, 'A', libtcod.white, inventory=test_inventory)
		potions = get_carried_potions(test_player)
		self.assertEqual(len(potions), 2)

	def test_can_quaff_potion(self):
		test_potion = make_healing_potion()
		test_potion2 = make_poison_potion()
		test_inventory = Inventory(10)
		test_inventory.items.append(test_potion)
		test_inventory.items.append(test_potion2)
		test_player = entity.Entity(1, 1, 'A', libtcod.white, inventory=test_inventory)
		potions = get_carried_potions(test_player)
		used_potion = potions[0]
		player_turn_results = []
		player_turn_results.extend(test_player.inventory.use(used_potion))
		self.assertNotEqual(player_turn_results, 0)

class PickupTests(unittest.TestCase):
	def test_can_pickup_item(self):
		test_bow = EquippableFactory.make_shortbow()
		test_inventory = Inventory(10)
		test_player = entity.Entity(1, 1, 'A', libtcod.white, inventory=test_inventory)
		entities = []
		entities.append(test_player)
		entities.append(test_bow)
		player_turn_results = []
		player_turn_results.extend(pickup_item(test_player, entities))
		self.assertTrue('item_added' in player_turn_results[0])

	def test_picking_up_can_stack_quantity(self):
		test_inventory = Inventory(10)
		test_player = entity.Entity(1, 1, 'A', libtcod.white, inventory=test_inventory)
		self.assertEqual(len(test_player.inventory.items), 0)
		test_arrows = EquippableFactory.make_arrows(1, 1, 5)
		test_player.inventory.items.append(test_arrows)
		self.assertEqual(test_player.inventory.items[0].item.quantity, 5)
		self.assertEqual(len(test_player.inventory.items), 1)
		test_arrows_2 = EquippableFactory.make_arrows(1,1, 2)
		test_player.inventory.add_item(test_arrows_2)
		self.assertEqual(len(test_player.inventory.items), 1)
		self.assertEqual(test_player.inventory.items[0].item.quantity, 7)

class FeatTests(unittest.TestCase):
	def test_can_get_current_feats(self):
		test_performer = Performer()
		test_player = entity.Entity(1, 1, 'A', libtcod.white, performer=test_performer)
		self.assertEqual(len(test_player.performer.feat_list), 0)

	def test_can_get_targetable_entities(self):
		test_player_fighter = Fighter()
		test_player = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_player_fighter)
		fighter_component = Fighter()
		test_monster = entity.Entity(1, 0, 'B', libtcod.white, fighter=fighter_component)
		entities = [test_player, test_monster]
		self.assertEqual(len(get_targetable_entities_in_range(test_player, 5, entities)), 1)

	def test_can_get_available_feats(self):
		pass

	def test_can_learn_unlocked_feat(self):
		pass

	def test_cannot_learn_locked_feat(self):
		pass

class DRTests(unittest.TestCase):
	def test_can_get_base_DR(self):
		test_equipment = Equipment()
		test_fighter = Fighter()
		test_player = test_player = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_fighter, equipment=test_equipment)
		self.assertEqual(test_player.fighter.DR, 0)
		test_fighter2 = Fighter(base_DR=2)
		test_player2 = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_fighter2, equipment=test_equipment)
		self.assertEqual(test_player2.fighter.DR, 2)

	def test_can_get_DR_from_equipment(self):
		test_equipment = Equipment()
		test_fighter = Fighter()
		test_player = test_player = entity.Entity(1, 1, 'A', libtcod.white, fighter=test_fighter, equipment=test_equipment)
		self.assertEqual(test_player.fighter.DR, 0)
		test_armor = EquippableFactory.make_padded_armor()
		test_equipment.body = test_armor
		self.assertEqual(test_player.fighter.DR, 1)


if __name__ == "__main__":
	unittest.main()
