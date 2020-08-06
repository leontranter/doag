from equipment_slots import EquipmentSlots
from damage_types import DamageTypes
from loader_functions.constants import WeaponTypes, WeaponCategories, AmmunitionTypes
from entity import Entity
from components.meleeweapon import MeleeWeapon
from components.missileweapon import MissileWeapon
from components.name import Name
from components.item import Item
from components.ammunition import Ammunition
import tcod as libtcod

class Equippable:
	def __init__(self, slot, DR_bonus=0, max_hp_bonus=0, two_handed=False, isShield=False, hit_modifier=0, physical_damage_modifier=0):
		self.slot = slot
		self.DR_bonus = DR_bonus
		self.max_hp_bonus = max_hp_bonus
		self.two_handed = two_handed
		self.isShield = isShield
		self.hit_modifier = hit_modifier
		self.physical_damage_modifier = physical_damage_modifier

def make_dropped_missile(missile_type, location):
	missiles = {"Arrows": EquippableFactory.make_arrows, "Bolts": EquippableFactory.make_bolts}
	dropped_missile = missiles[missile_type](x=location[0], y=location[1], quantity=1)
	return dropped_missile

class EquippableFactory:

	def make_axe(x=1, y=1):
		axe_equippable = Equippable(EquipmentSlots.MAIN_HAND)
		axe_name = Name("Axe")
		axe_melee_weapon = MeleeWeapon(WeaponTypes.AXE, WeaponCategories.AXE, melee_attack_type="swing", melee_damage=(1,6,1), melee_damage_type=DamageTypes.SLASHING, min_strenght=12)
		axe_item = Item(8, 1)
		axe_entity = Entity(x, y, '(', libtcod.red, equippable=axe_equippable, melee_weapon=axe_melee_weapon, name=axe_name, item=axe_item)
		return axe_entity

	def make_mace(x=1, y=1):
		mace_equippable = Equippable(EquipmentSlots.MAIN_HAND)
		mace_name = Name("Mace")
		mace_melee_weapon = MeleeWeapon(WeaponTypes.MACE, WeaponCategories.MACE, melee_attack_type="swing", melee_damage=(1,6,2), melee_damage_type=DamageTypes.CRUSHING, min_strength=13)
		mace_item = Item(9, 1)
		mace_entity = Entity(x, y, '(', libtcod.dark, equippable=axe_equippable, melee_weapon=mace_melee_weapon, name=mace_name, item=mace_item)
		return mace_entity

	def make_dagger(x=1, y=1):
		dagger_equippable = Equippable(EquipmentSlots.MAIN_HAND)
		dagger_name = Name("Dagger")
		dagger_melee_weapon = MeleeWeapon(WeaponTypes.DAGGER, WeaponCategories.DAGGER, melee_attack_type="thrust", melee_damage=(1,4,0), melee_damage_type=DamageTypes.PIERCING, min_strength=7)
		dagger_item = Item(3, 1)
		dagger_entity = Entity(x, y, '(', libtcod.orange, equippable=dagger_equippable, melee_weapon=dagger_melee_weapon, name=dagger_name, item=dagger_item)
		return dagger_entity

	def make_longsword(x=1, y=1):
		sword_equippable = Equippable(EquipmentSlots.MAIN_HAND)
		sword_name = Name("Longsword")
		sword_melee_weapon = MeleeWeapon(WeaponTypes.LONGSWORD, WeaponCategories.SWORD, melee_attack_type="swing", melee_damage=(1,6,0), melee_damage_type=DamageTypes.SLASHING, min_strength=11)
		sword_item = Item(7, 1)
		sword_entity = Entity(x, y, '(', libtcod.sky, equippable=sword_equippable, melee_weapon=sword_melee_weapon, name=sword_name, item=sword_item)
		return sword_entity

	def make_greatsword(x=1, y=1):
		greatsword_equippable = Equippable(EquipmentSlots.MAIN_HAND, two_handed=True)
		greatsword_name = Name("Greatsword")
		greatsword_melee_weapon = MeleeWeapon(WeaponTypes.GREATSWORD, WeaponCategories.SWORD, melee_attack_type="swing", melee_damage=(2,5,0), melee_damage_type=DamageTypes.SLASHING, min_strength=14)
		greatsword_item = Item(14, 1)
		greatsword_entity = Entity(x, y, '(', libtcod.red, equippable=greatsword_equippable, melee_weapon=greatsword_melee_weapon, name=greatsword_name, item=greatsword_item)
		return greatsword_entity

	def make_rapier(x=1, y=1):
		rapier_equippable = Equippable(EquipmentSlots.MAIN_HAND)
		rapier_name = Name("Rapier")
		rapier_melee_weapon = MeleeWeapon(WeaponTypes.RAPIER, WeaponCategories.SWORD, melee_attack_type="thrust", melee_damage=(1,5,0), melee_damage_type=DamageTypes.PIERCING, min_strength=10)
		rapier_item = Item(7, 1)
		rapier_entity = Entity(x, y, '(', libtcod.green, equippable=rapier_equippable, melee_weapon=rapier_melee_weapon, name=rapier_name, item=rapier_item)
		return rapier_entity

	def make_shortbow(x=1, y=1):
		bow_equippable = Equippable(EquipmentSlots.MAIN_HAND, two_handed=True)
		bow_name = Name("Bow")
		bow_missile_weapon = MissileWeapon(WeaponTypes.SHORTBOW, WeaponCategories.BOW, missile_damage=(1, 6, 0), missile_damage_type=DamageTypes.PIERCING)
		bow_item = Item(6, 1)
		bow_entity = Entity(x, y, ')', libtcod.orange, equippable=bow_equippable, missile_weapon=bow_missile_weapon, name=bow_name, item=bow_item)
		return bow_entity

	def make_crossbow(x=1, y=1):
		crossbow_equippable = Equippable(EquipmentSlots.MAIN_HAND, two_handed=True)
		crossbow_name = Name("Crossbow")
		crossbow_missile_weapon = MissileWeapon(WeaponTypes.CROSSBOW, WeaponCategories.CROSSBOW, missile_damage=(1, 8, 0), missile_damage_type=DamageTypes.PIERCING)
		crossbow_item = Item(7, 1)
		crossbow_entity = Entity(x, y, ')', libtcod.red, equippable=crossbow_equippable, missile_weapon=crossbow_missile_weapon, name=crossbow_name, item=crossbow_item)
		return crossbow_entity

	def make_arrows(x=1, y=1, quantity=1):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION)
		arrows_name = Name("Arrow")
		arrows_item = Item(1, quantity)
		arrows_ammunition = Ammunition(AmmunitionTypes.ARROWS, WeaponCategories.BOW)
		arrows_entity = Entity(x, y, ')', libtcod.flame, equippable=arrows_equippable, name=arrows_name, item=arrows_item, ammunition=arrows_ammunition)
		return arrows_entity

	def make_bolts(x=1, y=1, quantity=1):
		arrows_equippable = Equippable(EquipmentSlots.AMMUNITION)
		bolts_name = Name("Bolts")
		bolts_item = Item(1, quantity)
		bolts_ammunition = Ammunition(AmmunitionTypes.BOLTS, WeaponCategories.CROSSBOW)
		bolts_entity = Entity(x, y, ')', libtcod.flame, equippable=crossbow_equippable, name=bolts_name, item=bolts_item, ammunition=bolts_ammunition)
		return bolts_entity

	def make_small_shield(x=1, y=1):
		small_shield_equippable = Equippable(EquipmentSlots.OFF_HAND, isShield=True)
		small_shield_name = Name("Small Shield")
		small_shield_item = Item(10, 1)
		small_shield_entity = Entity(x, y, '[', equippable=small_shield_equippable, name=small_shield_name, item=small_shield_item)
		return small_shield_entity

	def make_shield(x=1, y=1):
		shield_equippable = Equippable(EquipmentSlots.OFF_HAND, isShield=True)
		shield_name = Name("Shield")
		shield_item = Item(15, 1)
		shield_entity = Entity(x, y, '[', libtcod.green, equippable=shield_equippable, name=shield_name, item=shield_item)
		return shield_entity

	def make_tower_shield(x=1, y=1):
		towershield_equippable = Equippable(EquipmentSlots.OFF_HAND, isShield=True)
		tower_shield_name = Name("Tower Shield")
		tower_shield_item = Item(20, 1)
		tower_shield_entity = Entity(x, y, '[', libtcod.green, equippable=tower_shield_equippable, name=tower_shield_name, item=tower_shield_item)
		return tower_shield_entity
	
	def make_padded_armor(x=1, y=1):
		padded_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=1)
		padded_armor_name = Name("Padded Armor")
		padded_armor_item = Item(6, 1)
		padded_armor_entity = Entity(x, y, ')', libtcod.purple, equippable=padded_armor_equippable, name=padded_armor_name, item=padded_armor_item)
		return padded_armor_entity

	def make_leather_armor(x=1, y=1):
		leather_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=1)
		leather_armor_name = Name("Leather Armor")
		leather_armor_item = Item(12, 1)
		leather_armor_entity = Entity(x, y, ')', libtcod.purple, equippable=leather_armor_equippable, name=leather_armor_name, item=leather_armor_item)
		return leather_armor_entity

	def make_chain_armor(x=1, y=1):
		chain_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=2)
		chain_armor_name = Name("Chain Armor")
		chain_armor_item = Item(25, 1)
		chain_armor_entity = Entity(x, y, ')', libtcod.sky, equippable=padded_armor_equippable, name=chain_armor_name, item=chain_armor_item)
		return chain_armor_entity

	def make_scale_armor(x=1, y=1):
		scale_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=3)
		scale_armor_name = Name("Scale Armor")
		scale_armor_item = Item(35, 1)
		scale_armor_entity = Entity(x, y, ')', libtcod.sky, equippable=padded_armor_equippable, name=scale_armor_name, item=scale_armor_item)
		return scale_armor_entity		

	def make_plate_armor(x=1, y=1):
		plate_armor_equippable = Equippable(EquipmentSlots.BODY, DR_bonus=5)
		plate_armor_name = Name("Plate Armor")
		plate_armor_item = Item(45, 1)
		plate_armor_entity = Entity(x, y, ')', libtcod.darker, equippable=padded_armor_equippable, name=plate_armor_name, item=plate_armor_item)
		return plate_armor_entity