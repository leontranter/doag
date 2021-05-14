from enum import Enum, auto

class GameStates(Enum):
	PLAYERS_TURN = auto()
	ENEMY_TURN = auto()
	PLAYER_DEAD = auto()
	SHOW_INVENTORY = auto()
	DROP_INVENTORY = auto()
	TARGETING = auto()
	LEVEL_UP = auto()
	CHARACTER_SCREEN = auto()
	SPELLS_SCREEN = auto()
	POTION_SCREEN = auto()
	EQUIPMENT_SCREEN = auto()
	FEATS_SCREEN = auto()
	SKILLS_SCREEN = auto()