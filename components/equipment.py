from equipment_slots import EquipmentSlots

class Equipment:
	def __init__(self, main_hand=None, off_hand=None, body=None, ammunition=None):
		self.main_hand = main_hand
		self.off_hand = off_hand
		self.body = body
		self.ammunition = ammunition

	@property
	def max_hp_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.max_hp_bonus

		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.max_hp_bonus

		if self.body and self.body.equippable:
			bonus += self.body.equippable.max_hp_bonus

		if self.ammunition and self.ammunition.equippable:
			bonus += self.ammunition.equippable.max_hp_bonus

		return bonus

	@property
	def melee_damage_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.melee_damage_bonus
		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.melee_damage_bonus
		if self.body and self.body.equippable:
			bonus += self.body.equippable.melee_damage_bonus
		if self.ammunition and self.ammunition.equippable:
			bonus += self.ammunition.equippable.melee_damage_bonus			

		return bonus

	@property
	def missile_damage_bonus(self):
		bonus = 0
		
		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.missile_damage_bonus
		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.missile_damage_bonus
		if self.body and self.body.equippable:
			bonus += self.body.equippable.missile_damage_bonus
		if self.ammunition and self.ammunition.equippable:
			bonus += self.ammunition.equippable.missile_damage_bonus			

		return bonus

	@property
	def PD_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.PD_bonus
		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.PD_bonus
		if self.body and self.body.equippable:
			bonus += self.body.equippable.PD_bonus
		if self.ammunition and self.ammunition.equippable:
			bonus += self.ammunition.equippable.PD_bonus

		return bonus

	@property
	def DR_bonus(self):
		bonus = 0

		if self.main_hand and self.main_hand.equippable:
			bonus += self.main_hand.equippable.DR_bonus
		if self.off_hand and self.off_hand.equippable:
			bonus += self.off_hand.equippable.DR_bonus
		if self.body and self.body.equippable:
			bonus += self.body.equippable.DR_bonus
		if self.ammunition and self.ammunition.equippable:
			bonus += self.ammunition.equippable.DR_bonus

		return bonus


	def toggle_equip(self, equippable_entity):
		results = []
		slot = equippable_entity.equippable.slot
		if slot == EquipmentSlots.MAIN_HAND:
			equippable_entity, results = self.toggle_main_hand(equippable_entity, results)
		elif slot == EquipmentSlots.OFF_HAND:
			if self.off_hand == equippable_entity:
				self.off_hand = None
				results.append({'dequipped': equippable_entity})
			else:
				if self.main_hand and self.main_hand.equippable.two_handed:
					results.append({'fail_equip': "You can't equip your off-hand while wielding a 2-handed weapon."})
				else:
					if self.off_hand:
						results.append({'dequipped': self.off_hand})
					self.off_hand = equippable_entity
					results.append({'equipped': equippable_entity})
		elif slot == EquipmentSlots.BODY:
			equippable_entity, results = self.toggle_body(equippable_entity, results)
		elif slot == EquipmentSlots.AMMUNITION:
			equippable_entity, results = self.toggle_ammunition(equippable_entity, results)
		return results

	def getEquippedItems(self):
		equipped_items = []
		equipped_items.append(self.main_hand)
		equipped_items.append(self.off_hand)
		equipped_items.append(self.body)
		equipped_items.append(self.ammunition)
		return equipped_items

	def toggle_main_hand(self, equippable_entity, results):
		if self.main_hand == equippable_entity:
			self.main_hand = None
			results.append({'dequipped': equippable_entity})
		else:
			if equippable_entity.equippable.two_handed:
				if self.off_hand:
					results.append({'fail_equip': "You can't equip a 2-handed weapon while you have your off-hand equipped."})
				else:
					if self.main_hand:
						results.append({'dequipped': self.main_hand})
					self.main_hand = equippable_entity
					results.append({'equipped': equippable_entity})	
			else:
				if self.main_hand:
					results.append({'dequipped': self.main_hand})
				self.main_hand = equippable_entity
				results.append({'equipped': equippable_entity})
		return equippable_entity, results

	# TGDO: do I need this??
	def toggle_off_hand(self, equippable_entity, results):
		pass
	
	def toggle_body(self, equippable_entity, results):
		if self.body == equippable_entity:
			self.body = None
			results.append({'dequipped': equippable_entity})
		else:
			if self.body:
				results.append({'dequipped': equippable_entity})
			self.body = equippable_entity
			results.append({'equipped': equippable_entity})
		return equippable_entity, results

	def toggle_ammunition(self, equippable_entity, results):
		if self.ammunition == equippable_entity:
			self.ammunition = None
			results.append({'dequipped': equippable_entity})
		else:
			if self.ammunition:
				results.append({'dequipped': equippable_entity})
			self.ammunition = equippable_entity
			results.append({'equipped': equippable_entity})
		return equippable_entity, results