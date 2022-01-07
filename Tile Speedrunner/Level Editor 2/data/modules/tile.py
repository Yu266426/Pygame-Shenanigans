import pygame

from data.modules.images import TILE_IMAGES
from data.modules.settings import SCREEN_HEIGHT, TILE_SIZE


class Tile:
	def __init__(self, pos, tile_name, type, size=TILE_SIZE, screen_height=SCREEN_HEIGHT):
		self.type = tile_name

		self.image = pygame.transform.scale(TILE_IMAGES[tile_name][type], (size, size))

		self.rect = self.image.get_rect(topleft=(pos[0] * size, ((screen_height / size) - pos[1] - 1) * size))

	def draw(self, display, scroll):
		display.blit(self.image, self.rect.topleft - scroll)
