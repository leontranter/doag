from enum import Enum, auto
from feats import Feat
import tcod as libtcod
from systems.skill_manager import SkillNames
from attack_types import AttackTypes
from game_messages import Message
from systems.attack import attack

def add_feat(player, feat):
	player.performer.feat_list.append(feat)

def get_available_feats(player):
	return []

def make_savage_strike():
	feat = Feat(FeatNames.SAVAGE_STRIKE, "Savage Strike", SkillNames.SWORD, 2, 3, perform_savage_strike, True, Message('Left-click a target to strike, or right-click to cancel.', libtcod.light_cyan), 1)
	return feat

def perform(entity, feat, **kwargs):
	results = []
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')
	if feat.stamina_cost > entity.stats.sp:
		results.append({'message': Message("You don't have enough stamina to perform that feat.")})
		return results

	if feat.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
		results.append({'feat_targeting': feat})
	else:
		kwargs = {**feat.function_kwargs, **kwargs}
		entity.stats.sp -= feat.stamina_cost
		feat_perform_results = feat.use_function(entity, **kwargs)

		results.extend(feat_perform_results)
		results.append({'performed': feat.name})
	return results

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
	feat_results = attack(attacker, target, AttackTypes.MELEE, 10, 10) 
	results.extend(feat_results)
	return results

class FeatNames(Enum):
	SAVAGE_STRIKE = auto()