from data.modules.level_manager import LevelManager


class Game:
	def __init__(self, screen):
		self.screen = screen

		self.levels = LevelManager(self.screen)

		self.game_state = "game"

	def game(self, delta):
		self.levels.update(delta)

	def update(self, delta):
		if self.game_state == "game":
			self.game(delta)
		else:
			raise ValueError(f"game_state: '{self.game_state}' is not valid")
