import math
import tcod as libtcod
from render_functions import RenderOrder

class Entity:
	"""
	A generic object for anything
	"""
	def __init__(self, x, y, char, color, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, item=None, inventory=None, stairs=None, level=None, equipment=None,
		equippable=None, caster=None, stats=None, defender=None, skills=None, melee_weapon=None, missile_weapon=None, name=None, identified=None, consumable=None):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.blocks = blocks
		self.render_order = render_order
		self.fighter = fighter
		self.ai = ai
		self.item = item
		self.inventory = inventory
		self.stairs = stairs
		self.level = level
		self.equipment = equipment
		self.equippable = equippable
		self.caster = caster
		self.stats = stats
		self.defender = defender
		self.skills = skills
		self.melee_weapon = melee_weapon
		self.missile_weapon = missile_weapon
		self.name = name
		self.identified = identified
		self.consumable = consumable

		if self.fighter:
			self.fighter.owner = self
		if self.ai:
			self.ai.owner = self
		if self.item:
			self.item.owner = self
		if self.inventory:
			self.inventory.owner = self
		if self.stairs:
			self.stairs.owner = self
		if self.level:
			self.level.owner = self
		if self.equipment:
			self.equipment.owner = self
		if self.equippable:
			self.equippable.owner = self
		if caster:
			self.caster.owner = self
		if stats:
			self.stats.owner = self
		if defender:
			self.defender.owner = self
		if skills:
			self.skills.owner = self
		if melee_weapon:
			self.melee_weapon.owner = self
		if missile_weapon:
			self.missile_weapon.owner = self
		if name:
			self.name.owner = self
		if identified:
			self.identified.owner = self
		if self.consumable:
			self.consumable.owner = self