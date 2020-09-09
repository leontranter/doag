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
	feat = Feat(FeatNames.SAVAGE_STRIKE, "Savage Strike", SkillNames.SWORD, 2, 3, perform_savage_strike, True, Message('Left-click a target to strike, or right-click to cancel.', libtcod.light_cyan), 1, feat_attack_modifier=2, feat_damage_modifier=2)
	return feat

def attempt_feat(entity, feat, **kwargs):
	results = []
	if feat.stamina_cost > entity.stats.sp:
		results.append({'message': Message("You don't have enough stamina to perform that feat.")})
		return results
	
	if not feat.targeting:
		kwargs = {**feat.function_kwargs, **kwargs}
		results.extend(perform_feat(entity, feat, None, results, **kwargs))
		return results

	entities = kwargs.get('entities')
	target_x, target_y = kwargs.get('target_x'), kwargs.get('target_y')

	if len(get_targetable_entities_in_range(entity, feat.feat_range, entities)) == 1:
		target = get_targetable_entities_in_range(entity, feat.feat_range, entities)[0]
		kwargs = {**feat.function_kwargs, **kwargs}
		results = perform_feat(entity, feat, target, results, **kwargs)
	
	elif not (target_x or target_y):
		results.append({'feat_targeting': feat})
	
	elif int(distance(entity, target_x, target_y)) > feat.feat_range:
		results.append({'message': Message("That target is out of range for the selected feat.")})
	
	else:
		for targetable_entity in entities:
			if targetable_entity.x == target_x and targetable_entity.y == target_y and entity.fighter:
				target = targetable_entity
				break
		else:
			results.append({'message': Message('There are no valid targets there.')})
			return results
		kwargs = {**feat.function_kwargs, **kwargs}
		results = perform_feat(entity, feat, target, results, **kwargs)
	
	return results

def perform_feat(entity, feat, target, results, **kwargs):
	entity.stats.sp -= feat.stamina_cost
	results.extend(feat.use_function(entity, target, **kwargs))
	results.append({'performed': feat.name})
	return results

def perform_savage_strike(attacker, target, **kwargs):
	feat_attack_modifier = kwargs.get('feat_attack_modifier')
	feat_damage_modifier = kwargs.get('feat_damage_modifier')
	print(f"feat attack mod is {feat_attack_modifier}")
	results = []
	results.extend(attack(attacker, target, AttackTypes.MELEE, feat_attack_modifier, feat_damage_modifier))
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