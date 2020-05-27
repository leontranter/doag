from enum import Enum

class DamageTypes(Enum):
	CRUSHING = 1
	CUTTING = 2
	IMPALING = 3
	BURNING = 4

damage_type_modifiers = {DamageTypes.CRUSHING: 1.0, DamageTypes.CUTTING: 1.5, DamageTypes.IMPALING: 2, DamageTypes.BURNING: 1.5}