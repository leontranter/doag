from equipment_slots import EquipmentSlots
from damage_types import DamageTypes
from loader_functions.constants import WeaponTypes
from entity import Entity
from components.meleeweapon import MeleeWeapon
from components.missileweapon import MissileWeapon
import tcod as libtcod

class Equippable:
	def __init__(self, slot, DR_bonus=0, max_hp_bonus=0, two_handed=False, quantity=0, isShield=False, weight=1, missile_damage_bonus=0):
		self.slot = slot
		self.DR_bonus = DR_bonus
		self.max_hp_bonus = max_hp_bonus
		self.two_handed = two_handed
		self.quantity = quantity
		self.isShield = isShield
		self.weight = weight
		self.missile_damage_bonus = missile_damage_bonus

def make_dropped_missile(missile_type, location):
	missiles = {"Arrows": EquippableFactory.makeArrows, "Bolts": EquippableFactory.makeBolts}
	dropped_missile = missiles[missile_type](x=location[0], y=location[1], quantity=1)
	return dropped_missile

class EquippableFactory:

	def makeAxe(x=1, y=1):
		axe_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=8)
		axe_melee_weapon = MeleeWeapon(WeaponTypes.AXE, "swing", 2, DamageTypes.SLASHING, min_strenght=12)
		axe_entity = Entity(x, y, '(', libtcod.red, 'Axe', equippable=axe_equippable, melee_weapon=axe_melee_weapon)
		return axe_entity

	def makeMace(x=1, y=1):
		mace_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=10)
		mace_melee_weapon = MeleeWeapon(WeaponTypes.AXE, "swing", 3, DamageTypes.CRUSHING, min_strength=13)
		mace_entity = Entity(x, y, '(', libtcod.dark, 'Mace', equippable=axe_equippable, melee_weapon=mace_melee_weapon)
		return mace_entity

	def makeDagger(x=1, y=1):
		dagger_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=3)
		dagger_melee_weapon = MeleeWeapon(WeaponTypes.DAGGER, "thrust", 0, DamageTypes.PIERCING, min_strength=7)
		dagger_entity = Entity(x, y, '(', libtcod.orange, 'Dagger', equippable=dagger_equippable, melee_weapon=dagger_melee_weapon)
		return dagger_entity

	def makeBroadSword(x=1, y=1):
		sword_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=7)
		sword_melee_weapon = MeleeWeapon(WeaponTypes.SWORD, "swing", 1, DamageTypes.SLASHING, min_strength=11)
		sword_entity = Entity(x, y, '(', libtcod.sky, 'Sword', equippable=sword_equippable, melee_weapon=sword_melee_weapon)
		return sword_entity

	def makeGreatSword(x=1, y=1):
		greatsword_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=18, two_handed=True)
		greatsword_melee_weapon = MeleeWeapon(weapon_type = WeaponTypes.SWORD, melee_attack_type="swing", melee_damage_bonus=3, melee_damage_type=DamageTypes.SLASHING, min_strength=14)
		greatsword_entity = Entity(x, y, '(', libtcod.red, 'Greatsword', equippable=greatsword_equippable, melee_weapon=greatsword_melee_weapon)
		return greatsword_entity

	def makeRapier(x=1, y=1):
		rapier_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=10)
		rapier_melee_weapon = MeleeWeapon(weapon_type=WeaponTypes.SWORD, melee_attack_type="thrust", melee_damage_bonus=1, melee_damage_type=DamageTypes.PIERCING, min_strength=10)
		rapier_entity = Entity(x, y, '(', libtcod.green, 'Rapier', equippable=rapier_equippable, melee_weapon=rapier_melee_weapon)
		return rapier_entity

	def makeBow(x=1, y=1):
		bow_equippable = Equippable(EquipmentSlots.MAIN_HAND, two_handed=True, weight=6)
		bow_missile_weapon = MissileWeapon(weapon_type=WeaponTypes.CROSSBOW, missile_damage=(1, 0), missile_damage_type=DamageTypes.PIERCING)
		bow_entity = Entity(x, y, ')', libtcod.orange, 'Bow', equippable=bow_equippable, missile_weapon=bow_missile_weapon)
		return bow_entity

	def makeCrossBow(x=1, y=1):
		crossbow_equippable = Equippable(EquipmentSlots.MAIN_HAND, two_handed=True, weight=7)
		crossbow_missile_weapon = MissileWeapon(weapon_type=WeaponTypes.CROSSBOW, missile_damage=(1, 3), missile_damage_type=DamageTypes.PIERCING)
		crossbow_entity = Entity(x, y, ')', libtcod.red, 'Crossbow', equippable = crossbow_equippable, missile_weapon=crossbow_missile_weapon)
		return crossbow_entity

	def makeArrows(x=1, y=1, quantity=10):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION, missile_damage_bonus=1, quantity=quantity)
		arrows_entity = Entity(x, y, ')', libtcod.flame, 'Arrows', equippable = arrows_equippable)
		return arrows_entity

	def makeSteelArrows(x=1, y=1, quantity=10):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION, missile_damage_bonus=2, quantity=quantity)
		arrows_entity = Entity(x, y, ')', libtcod.flame, 'Steel Arrows', equippable = arrows_equippable)
		return arrows_entity	

	def makeObsidianArrows(x=1, y=1, quantity=10):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION, missile_damage_bonus=3, quantity=quantity)
		arrows_entity = Entity(x, y, ')', libtcod.flame, 'Obsidian Arrows', equippable = arrows_equippable)
		return arrows_entity

	def makeBolts(x=1, y=1, quantity=10):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION, missile_damage_bonus=1, quantity=quantity)
		bolts_entity = Entity(x, y, ')', libtcod.flame, 'Bolts', equippable = crossbow_equippable)
		return bolts_entity

	def makeSmallShield(x=1, y=1):
		small_shield_equippable = Equippable(EquipmentSlots.OFF_HAND, isShield=True, weight=10)
		small_shield_entity = Entity(x, y, '[', 'Small Shield', equippable=small_shield_equippable)
		return small_shield_entity

	def makeShield(x=1, y=1):
		shield_equippable = Equippable(EquipmentSlots.OFF_HAND, isShield=True, weight=15)
		shield_entity = Entity(x, y, '[', libtcod.green, 'Shield', equippable=shield_equippable)
		return shield_entity

	def makeTowerShield(x=1, y=1):
		towershield_equippable = Equippable(EquipmentSlots.OFF_HAND, isShield=True, weight=20)
		tower_shield_entity = Entity(x, y, '[', libtcod.green, 'Tower Shield', equippable=tower_shield_equippable)
		return tower_shield_entity
	
	def makePaddedArmor(x=1, y=1):
		padded_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=1, weight=6)
		padded_armor_entity = Entity(x, y, ')', libtcod.purple, 'Padded Armor', equippable=padded_armor_equippable)
		return padded_armor_entity

	def makeLeatherArmor(x=1, y=1):
		leather_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=1, weight=12)
		leather_armor_entity = Entity(x, y, ')', libtcod.purple, 'Padded Armor', equippable=leather_armor_equippable)
		return leather_armor_entity

	def makeChainArmor(x=1, y=1):
		chain_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=2, weight=25)
		chain_armor_entity = Entity(x, y, ')', libtcod.sky, 'Chain Armor', equippable=padded_armor_equippable)
		return chain_armor_entity

	def makeScaleArmor(x=1, y=1):
		scale_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=3, weight=35)
		scale_armor_entity = Entity(x, y, ')', libtcod.sky, 'Chain Armor', equippable=padded_armor_equippable)
		return scale_armor_entity		

	def makePlateArmor(x=1, y=1):
		plate_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=5, weight=50)
		plate_armor_entity = Entity(x, y, ')', libtcod.darker, 'Plate Armor', equippable=padded_armor_equippable)
		return plate_armor_entity
