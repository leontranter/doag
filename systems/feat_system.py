from enum import Enum, auto
from feats import Feat
import tcod as libtcod
from systems.skill_manager import SkillNames
from attack_types import AttackTypes
from game_messages import Message
from systems.attack import attack
from systems.move_system import distance

def add_feat(player, feat):
	player.performer.feat_list.append(feat)

def get_available_feats(player):
	return []

def make_savage_strike():
	feat = Feat(FeatNames.SAVAGE_STRIKE, "Savage Strike", SkillNames.SWORD, 2, 3, perform_savage_strike, True, Message('Left-click a target to strike, or right-click to cancel.', libtcod.light_cyan), 1)
	return feat

def attempt_feat(entity, feat, **kwargs):
	results = []
	if feat.stamina_cost > entity.stats.sp:
		results.append({'message': Message("You don't have enough stamina to perform that feat.")})
		return results
	
	target_x, target_y = kwargs.get('target_x'), kwargs.get('target_y')
	entities = kwargs.get('entities')

	if feat.targeting and len(get_targetable_entities_in_range(entity, feat.feat_range, entities)) == 1:
		print("instant targeting!")
		target = get_targetable_entities_in_range(entity, feat.feat_range, entities)[0]
		target_dict = {'target_x': target.x, 'target_y': target.y}
		kwargs = {**feat.function_kwargs, **kwargs, **target_dict}
		results.extend(perform_feat(entity, feat, results, **kwargs))
	
	elif feat.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
		results.append({'feat_targeting': feat})
	
	elif feat.targeting and int(distance(entity, target_x, target_y)) > feat.feat_range:
		results.append({'message': Message("That target is out of range for the selected feat.")})
	
	else:
		kwargs = {**feat.function_kwargs, **kwargs}
		results.extend(perform_feat(entity, feat, results, **kwargs))
	
	return results

def perform_feat(entity, feat, results, **kwargs):
	entity.stats.sp -= feat.stamina_cost
	results.extend(feat.use_function(entity, **kwargs))
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

def get_targetable_entities_in_range(entity, feat_range, entities):
	targetable_entities = []
	for targetable_entity in entities:
		if int(distance(entity, targetable_entity.x, targetable_entity.y)) <= feat_range and targetable_entity.fighter:
			if (targetable_entity.x, targetable_entity.y) != (entity.x, entity.y):
				targetable_entities.append(targetable_entity)
	return targetable_entities

class FeatNames(Enum):
	SAVAGE_STRIKE = auto()