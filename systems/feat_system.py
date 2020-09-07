from enum import Enum, auto
from feats import Feat
from skills import SkillNames
from attack_types import AttackTypes

def add_feat(player, feat):
	player.performer.feat_list.append(feat)

def get_available_feats(player):
	return []

def make_savage_strike():
	feat = Feat(FeatNames.SAVAGE_STRIKE, "Savage Strike", SkillNames.SWORD, 2, 3, perform_savage_strike, True, "Choose a target")
	return feat

def perform_savage_strike(*args, **kwargs):
	attacker=args[0]
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage')
	feat_range = kwargs.get('feat_range')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')

	results = []
	for entity in entities:
		if entity.x == target_x and entity.y == target_y and entity.fighter:
			target = entity
			break
	else:
		results.append({'message': Message('There are no valid targets there.')})
		return results

	results.extend(attacker, target, AttackTypes.MELEE, 10, 10)
	return results

class FeatNames(Enum):
	SAVAGE_STRIKE = auto()