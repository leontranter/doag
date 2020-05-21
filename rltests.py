import unittest
import map_objects.game_map as maps
import engine
import map_objects.tile
import entity
import tcod as libtcod
import map_objects.rectangle as rectangle
from components.fighter import Fighter
from components.caster import Caster

class EntityTests(unittest.TestCase):
	def test_can_make_entity(self):
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player")
		self.assertEqual(test_entity.x, 1)

	def test_can_make_entity_with_fighter(self):
		test_fighter = Fighter(100, 5, 10)
		test_entity = entity.Entity(1, 1, 'A', libtcod.white, "Player", fighter=test_fighter)
		self.assertEqual(test_entity.fighter, test_fighter)
		self.assertEqual(test_entity.fighter.hp, 100)
		self.assertEqual(test_entity.fighter.max_hp, 100)
		self.assertEqual(test_entity.fighter.defense, 5)
		self.assertEqual(test_entity.fighter.power, 10)

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



class MapTests(unittest.TestCase):
	def test_can_make_map(self):
		test_map = maps.GameMap(80, 45)
		self.assertEqual(test_map.width, 80)
		self.assertEqual(test_map.height, 45)
		self.assertEqual(len(test_map.tiles), 80)
		self.assertEqual(len(test_map.tiles[0]), 45)

if __name__ == "__main__":
	unittest.main()
