import pygame

from data.modules.images import TILE_IMAGES
from data.modules.settings import SCREEN_HEIGHT, TILE_SIZE


class Tile:
	def __init__(self, pos, tile_name, type):
		self.type = tile_name

		self.image = TILE_IMAGES[tile_name][type]

		self.rect = self.image.get_rect(topleft=(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))

	def draw(self, display, scroll):
		display.blit(self.image, (self.rect.topleft[0] - scroll.x, self.rect.topleft[1] - scroll.y))
