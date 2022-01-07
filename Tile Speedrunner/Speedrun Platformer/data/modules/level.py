import pygame

from data.modules.helper import read_from_json
from data.modules.player import Player
from data.modules.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from data.modules.tile_list import TileList


class Level:
	def __init__(self, level_name):
		self.level_name = level_name

		self.tiles = None
		self.player = None

		self.scroll = pygame.Vector2(0, 0)

		self.initialize_level()

	def initialize_level(self):
		json = read_from_json(self.level_name)

		self.tiles = TileList((json["width"], json["height"]), json["tiles"])

		self.player = Player((json["player_x"], json["player_y"]))

	def get_scroll(self, delta):
		target_x = self.player.rect.center[0] - SCREEN_WIDTH / 2
		target_y = self.player.rect.center[1] - SCREEN_HEIGHT / 2

		self.scroll += pygame.Vector2(round((target_x - self.scroll.x) / 10, 3), round((target_y - self.scroll.y) / 10, 3)) * delta

		if self.scroll.x < 0:
			self.scroll.x = 0
		if self.scroll.y > 0:
			self.scroll.y = 0

	def update(self, delta):
		self.get_scroll(delta)

		self.player.update(delta, self.tiles.list)

	def draw(self, screen):
		self.tiles.draw(screen, self.scroll)

		self.player.draw(screen, self.scroll)
