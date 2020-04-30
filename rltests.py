import unittest
import map_objects.game_map as maps
import engine
import map_objects.tile
import entity
import tcod as libtcod
import map_objects.rectangle as rectangle

class EntityTests(unittest.TestCase):
	def test_can_make_entity(self):
		test_entity = entity.Entity(1, 1, 'A', libtcod.white)
		self.assertEqual(test_entity.x, 1)

class MapTests(unittest.TestCase):
	def test_can_make_map(self):
		test_map = maps.GameMap(80, 45)
		self.assertEqual(test_map.width, 80)
		self.assertEqual(test_map.height, 45)
		self.assertEqual(len(test_map.tiles), 80)
		self.assertEqual(len(test_map.tiles[0]), 45)

	def test_map_is_mainly_blocked(self):
		test_map2 = maps.GameMap(80, 45)
		self.assertEqual(test_map2.tiles[0][0].blocked, True)
		self.assertEqual(test_map2.tiles[0][0].block_sight, True)
		test_map2.make_map()
		self.assertEqual(test_map2.tiles[21][16].blocked, False)
		self.assertEqual(test_map2.tiles[21][16].block_sight, False)

	def test_can_make_h_tunnel(self):
		test_map3 = maps.GameMap(80, 45)
		self.assertEqual(test_map3.tiles[25][23].blocked, True)
		self.assertEqual(test_map3.tiles[25][23].block_sight, True)
		test_map3.make_map()
		self.assertEqual(test_map3.tiles[25][23].blocked, False)
		self.assertEqual(test_map3.tiles[25][23].blocked, False)

if __name__ == "__main__":
	unittest.main()