from data.modules.level import Level
from data.modules.settings import LEVEL_LIST


class LevelManager:
	def __init__(self, screen):
		self.level_number = 0

		self.level_name = LEVEL_LIST[self.level_number]

		self.level = Level(self.level_name)

		self.screen = screen

	def next_level(self):
		# TODO: have a check if it's the last level
		self.level_number += 1
		self.level_name = LEVEL_LIST[self.level_number]
		self.level = Level(self.level_name)

	def update(self, delta):
		self.level.update(delta)

		self.level.draw(self.screen)
