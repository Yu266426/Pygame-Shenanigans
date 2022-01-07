import pygame

from data.modules.images import TILE_IMAGES
from data.modules.tile import Tile


class Selector:
	def __init__(self):
		self.display = pygame.Surface((800, 200))

		self.scroll = pygame.Vector2(0, 0)

		self.tiles = []
		self.get_tiles()

		self.selected = 0

	def get_tiles(self):
		for key in TILE_IMAGES.keys():
			self.tiles.append(Tile((len(self.tiles), 0), key, f"{key}_t_b_l_r", size=200, screen_height=200))

	def outline_selected(self):
		pygame.draw.rect(self.display, (100, 200, 100), (self.selected * 200 + 1, 1, 200 - 2, 200 - 2), 2)

	def select_tile(self, mouse_pos):
		tile = int(mouse_pos[0] / 200)
		if 0 <= tile < len(self.tiles):
			self.selected = tile

	def draw_to_display(self):
		self.display.fill((20, 20, 20))

		for tile in self.tiles:
			tile.draw(self.display, self.scroll)

		self.outline_selected()

	@property
	def selected_tile(self):
		return self.tiles[self.selected].type

	def update(self):
		pass

	def draw(self, screen):
		self.draw_to_display()
		screen.blit(self.display, (0, 500))
