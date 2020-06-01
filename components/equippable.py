from equipment_slots import EquipmentSlots
from damage_types import DamageTypes
from loader_functions.constants import WeaponTypes
from entity import Entity
from components import MeleeWeapon
import tcod as libtcod

class Equippable:
	def __init__(self, slot, DR_bonus=0, PD_bonus=0, max_hp_bonus=0, two_handed=False, missile_damage=None, missile_damage_type=None, missile_damage_bonus=0, quantity=0, isShield=False, weight=1):
		self.slot = slot
		self.DR_bonus = DR_bonus
		self.PD_bonus = PD_bonus
		self.max_hp_bonus = max_hp_bonus
		self.two_handed = two_handed
		self.missile_damage = missile_damage
		self.missile_damage_type = missile_damage_type
		self.missile_damage_bonus = missile_damage_bonus
		self.quantity = quantity
		self.isShield = isShield
		self.weight = weight

def make_dropped_missile(missile_type, location):
	temp_equippable_missile = EquippableFactory.makeArrows(quantity=1)
	temp_entity = Entity(location[0], location[1], '(', libtcod.red, 'Arrows', equippable=temp_equippable_missile)
	return temp_entity

class EquippableFactory:

	def makeAxe():
		tempEquippable = Equippable(EquipmentSlots.MAIN_HAND, WeaponTypes.AXE, melee_attack_type="swing", melee_damage_bonus=2, melee_damage_type=DamageTypes.CUTTING, weight=4)
		tempMeleeWeapon = MeleeWeapon(WeaponTypes.AXE, "swing", 2, DamageTypes.CUTTING)
		return tempEquippable

	def makeMace():
		tempEquippable = Equippable(EquipmentSlots.MAIN_HAND, WeaponTypes.AXE, melee_attack_type="swing", melee_damage_bonus=3, melee_damage_type=DamageTypes.CRUSHING, weight=4)
		return tempEquippable		

	def makeDagger():
		tempEquippable = Equippable(EquipmentSlots.MAIN_HAND, WeaponTypes.DAGGER, melee_attack_type="thrust", melee_damage_bonus=0, melee_damage_type=DamageTypes.IMPALING)
		return tempEquippable

	def makeBroadSword():
		tempEquippable = Equippable(EquipmentSlots.MAIN_HAND, WeaponTypes.SWORD, melee_attack_type="swing", melee_damage_bonus=1, melee_damage_type=DamageTypes.CUTTING)
		return tempEquippable

	def makeSmallShield():
		tempEquippable = Equippable(EquipmentSlots.OFF_HAND, PD_bonus=1, isShield=True)
		return tempEquippable

	def makeShield():
		tempEquippable = Equippable(EquipmentSlots.OFF_HAND, PD_bonus=2, isShield=True)
		return tempEquippable

	def makeTowerShield():
		tempEquippable = Equippable(EquipmentSlots.OFF_HAND, PD_bonus=3, isShield=True)
		return tempEquippable
	
	def makeLeatherArmor():
		tempEquippable = Equippable(EquipmentSlots.BODY, PD_bonus=1, DR_bonus=1)
		return tempEquippable

	def makeChainArmor():
		tempEquippable = Equippable(EquipmentSlots.BODY, PD_bonus=2, DR_bonus=2)
		return tempEquippable

	def makePlateArmor():
		tempEquippable = Equippable(EquipmentSlots.BODY, PD_bonus=3, DR_bonus=4)
		return tempEquippable

	def makeZweihander():
		tempEquippable = Equippable(EquipmentSlots.MAIN_HAND, weapon_type = WeaponTypes.SWORD, melee_attack_type="swing", melee_damage_bonus=3, melee_damage_type=DamageTypes.CUTTING, two_handed=True)
		return tempEquippable

	def makeBow():
		tempEquippable = Equippable(EquipmentSlots.MAIN_HAND, weapon_type = WeaponTypes.BOW, melee_attack_type="swing", melee_damage_bonus=-3, melee_damage_type=DamageTypes.CRUSHING, two_handed=True, missile_damage=(1, 1), missile_damage_type=DamageTypes.IMPALING)
		return tempEquippable

	def makeCrossBow():
		tempEquippable = Equippable(EquipmentSlots.MAIN_HAND, weapon_type = WeaponTypes.CROSSBOW, melee_attack_type="swing", melee_damage_typee_bonus = -3, melee_damage_type=DamageTypes.CRUSHING, two_handed=True, missile_damage=(1, 3), missile_damage_type=DamageTypes.IMPALING)
		return tempEquippable		

	def makeArrows(quantity=10):
		tempEquippable = Equippable(EquipmentSlots.AMMUNITION, missile_damage_bonus=1, quantity=quantity)
		return tempEquippable		