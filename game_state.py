from game_states import GameStates

class GameState:
	def __init__(self):
		self.current_game_state = GameStates.PLAYERS_TURN
		self.previous_game_state = self.current_game_state