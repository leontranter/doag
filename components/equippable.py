from equipment_slots import EquipmentSlots
from damage_types import DamageTypes
from loader_functions.constants import WeaponTypes
from entity import Entity
from components.meleeweapon import MeleeWeapon
from components.missileweapon import MissileWeapon
from components.name import Name
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
	# TODO: dictionary needs to be MUCH bigger, and include all types of ammunition and corresponding functions
	# figure out what missile needs to be dropped, and call the corresponding factory function to make it
	missiles = {"Arrows": EquippableFactory.make_arrows, "Bolts": EquippableFactory.make_bolts}
	dropped_missile = missiles[missile_type](x=location[0], y=location[1], quantity=1)
	return dropped_missile

class EquippableFactory:

	def make_axe(x=1, y=1):
		axe_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=8)
		axe_name = Name("Axe")
		axe_melee_weapon = MeleeWeapon(WeaponTypes.AXE, "swing", 2, DamageTypes.SLASHING, min_strenght=12)
		axe_entity = Entity(x, y, '(', libtcod.red, equippable=axe_equippable, melee_weapon=axe_melee_weapon, name=axe_name)
		return axe_entity

	def make_mace(x=1, y=1):
		mace_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=10)
		mace_name = Name("Mace")
		mace_melee_weapon = MeleeWeapon(WeaponTypes.AXE, "swing", 3, DamageTypes.CRUSHING, min_strength=13)
		mace_entity = Entity(x, y, '(', libtcod.dark, equippable=axe_equippable, melee_weapon=mace_melee_weapon, name=mace_name)
		return mace_entity

	def make_dagger(x=1, y=1):
		dagger_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=3)
		dagger_name = Name("Dagger")
		dagger_melee_weapon = MeleeWeapon(WeaponTypes.DAGGER, "thrust", 0, DamageTypes.PIERCING, min_strength=7)
		dagger_entity = Entity(x, y, '(', libtcod.orange, equippable=dagger_equippable, melee_weapon=dagger_melee_weapon, name=dagger_name)
		return dagger_entity

	def make_sword(x=1, y=1):
		sword_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=7)
		sword_name = Name("Sword")
		sword_melee_weapon = MeleeWeapon(WeaponTypes.SWORD, "swing", 1, DamageTypes.SLASHING, min_strength=11)
		sword_entity = Entity(x, y, '(', libtcod.sky, equippable=sword_equippable, melee_weapon=sword_melee_weapon, name=sword_name)
		return sword_entity

	def make_greatsword(x=1, y=1):
		greatsword_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=18, two_handed=True)
		greatsword_name = Name("Greatsword")
		greatsword_melee_weapon = MeleeWeapon(weapon_type = WeaponTypes.SWORD, melee_attack_type="swing", melee_damage_bonus=3, melee_damage_type=DamageTypes.SLASHING, min_strength=14)
		greatsword_entity = Entity(x, y, '(', libtcod.red, equippable=greatsword_equippable, melee_weapon=greatsword_melee_weapon, name=greatsword_name)
		return greatsword_entity

	def make_rapier(x=1, y=1):
		rapier_equippable = Equippable(EquipmentSlots.MAIN_HAND, weight=10)
		rapier_name = Name("Rapier")
		rapier_melee_weapon = MeleeWeapon(weapon_type=WeaponTypes.SWORD, melee_attack_type="thrust", melee_damage_bonus=1, melee_damage_type=DamageTypes.PIERCING, min_strength=10)
		rapier_entity = Entity(x, y, '(', libtcod.green, equippable=rapier_equippable, melee_weapon=rapier_melee_weapon, name=rapier_name)
		return rapier_entity

	def make_bow(x=1, y=1):
		bow_equippable = Equippable(EquipmentSlots.MAIN_HAND, two_handed=True, weight=6)
		bow_name = Name("Bow")
		bow_missile_weapon = MissileWeapon(weapon_type=WeaponTypes.CROSSBOW, missile_damage=(1, 0), missile_damage_type=DamageTypes.PIERCING)
		bow_entity = Entity(x, y, ')', libtcod.orange, equippable=bow_equippable, missile_weapon=bow_missile_weapon, name=bow_name)
		return bow_entity

	def make_crossbow(x=1, y=1):
		crossbow_equippable = Equippable(EquipmentSlots.MAIN_HAND, two_handed=True, weight=7)
		crossbow_name = Name("Crossbow")
		crossbow_missile_weapon = MissileWeapon(weapon_type=WeaponTypes.CROSSBOW, missile_damage=(1, 3), missile_damage_type=DamageTypes.PIERCING)
		crossbow_entity = Entity(x, y, ')', libtcod.red, equippable = crossbow_equippable, missile_weapon=crossbow_missile_weapon, name=crossbow_name)
		return crossbow_entity

	def make_arrows(x=1, y=1, quantity=10):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION, missile_damage_bonus=1, quantity=quantity)
		arrows_name = Name("Arrows")
		arrows_entity = Entity(x, y, ')', libtcod.flame, equippable = arrows_equippable, name=arrows_name)
		return arrows_entity

	def make_steel_arrows(x=1, y=1, quantity=10):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION, missile_damage_bonus=2, quantity=quantity)
		steel_arrows_name = Name("Steel Arrows")
		arrows_entity = Entity(x, y, ')', libtcod.flame, equippable = arrows_equippable, name=steel_arrows_name)
		return arrows_entity	

	def make_obsidian_arrows(x=1, y=1, quantity=10):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION, missile_damage_bonus=3, quantity=quantity)
		obsidian_arrows_name = Name("Obsidian Arrows")
		arrows_entity = Entity(x, y, ')', libtcod.flame, equippable = arrows_equippable, name=obsidian_arrows_name)
		return arrows_entity

	def make_bolts(x=1, y=1, quantity=10):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION, missile_damage_bonus=1, quantity=quantity)
		bolts_name = Name("Bolts")
		bolts_entity = Entity(x, y, ')', libtcod.flame, equippable = crossbow_equippable, name=bolts_name)
		return bolts_entity

	def make_small_shield(x=1, y=1):
		small_shield_equippable = Equippable(EquipmentSlots.OFF_HAND, isShield=True, weight=10)
		small_shield_name = Name("Small Shield")
		small_shield_entity = Entity(x, y, '[', equippable=small_shield_equippable, name=small_shield_name)
		return small_shield_entity

	def make_shield(x=1, y=1):
		shield_equippable = Equippable(EquipmentSlots.OFF_HAND, isShield=True, weight=15)
		shield_name = Name("Shield")
		shield_entity = Entity(x, y, '[', libtcod.green, equippable=shield_equippable, name=shield_name)
		return shield_entity

	def make_tower_shield(x=1, y=1):
		towershield_equippable = Equippable(EquipmentSlots.OFF_HAND, isShield=True, weight=20)
		tower_shield_name = Name("Tower Shield")
		tower_shield_entity = Entity(x, y, '[', libtcod.green, equippable=tower_shield_equippable, name=tower_shield_name)
		return tower_shield_entity
	
	def make_padded_armor(x=1, y=1):
		padded_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=1, weight=6)
		padded_armor_name = Name("Padded Armor")
		padded_armor_entity = Entity(x, y, ')', libtcod.purple, equippable=padded_armor_equippable, name=padded_armor_name)
		return padded_armor_entity

	def make_leather_armor(x=1, y=1):
		leather_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=1, weight=12)
		leather_armor_name = Name("Leather Armor")
		leather_armor_entity = Entity(x, y, ')', libtcod.purple, equippable=leather_armor_equippable, name=leather_armor_name)
		return leather_armor_entity

	def make_chain_armor(x=1, y=1):
		chain_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=2, weight=25)
		chain_armor_name = Name("Chain Armor")
		chain_armor_entity = Entity(x, y, ')', libtcod.sky, equippable=padded_armor_equippable, name=chain_armor_name)
		return chain_armor_entity

	def make_scale_armor(x=1, y=1):
		scale_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=3, weight=35)
		scale_armor_name = Name("Scale Armor")
		scale_armor_entity = Entity(x, y, ')', libtcod.sky, equippable=padded_armor_equippable, name=scale_armor_name)
		return scale_armor_entity		

	def make_plate_armor(x=1, y=1):
		plate_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=5, weight=50)
		plate_armor_name = Name("Plate Armor")
		plate_armor_entity = Entity(x, y, ')', libtcod.darker, equippable=padded_armor_equippable, name=plate_armor_name)
		return plate_armor_entity