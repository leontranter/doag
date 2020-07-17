from enum import Enum

class DamageTypes(Enum):
	CRUSHING = 1
	SLASHING = 2
	PIERCING = 3
	BURNING = 4
	ACID = 5
	ELECTRICAL = 6

damage_type_modifiers = {DamageTypes.CRUSHING: 1.0, DamageTypes.SLASHING: 1.5, DamageTypes.PIERCING: 1.75, DamageTypes.BURNING: 1.5, DamageTypes.ACID: 1.5, DamageTypes.ELECTRICAL: 1.5}