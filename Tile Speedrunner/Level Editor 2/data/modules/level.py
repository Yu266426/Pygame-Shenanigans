import pygame

from data.modules.helper import read_from_json, draw_rect, get_tile_from_pos
from data.modules.tile_list import TileList


class Level:
	def __init__(self, file_path):
		self.display = pygame.Surface((800, 500))

		self.scroll = pygame.Vector2(0, 0)
		self.prev_scroll = pygame.Vector2(0, 0)

		level_data = read_from_json(file_path)
		self.tiles = TileList((level_data["width"], level_data["height"]), level_data["tiles"])

		self.prev_mouse_pos = [-1, -1]

	def move(self, pressed, mouse_pos):
		if pressed:
			if self.prev_mouse_pos[0] == self.prev_mouse_pos[1] == -1:
				self.prev_scroll.x = self.scroll.x
				self.prev_scroll.y = self.scroll.y

				self.prev_mouse_pos[0] = mouse_pos[0]
				self.prev_mouse_pos[1] = mouse_pos[1]
			else:
				self.scroll.x = self.prev_scroll.x + (self.prev_mouse_pos[0] - mouse_pos[0])
				self.scroll.y = self.prev_scroll.y + (self.prev_mouse_pos[1] - mouse_pos[1])

				if self.scroll.x < 0:
					self.scroll.x = 0
				if self.scroll.y > 0:
					self.scroll.y = 0
		else:
			self.prev_mouse_pos[0] = -1
			self.prev_mouse_pos[1] = -1

	def add_tile(self, mouse_pos, type):
		self.tiles.add_tile(get_tile_from_pos(mouse_pos + self.scroll), type)

	def remove_tile(self, mouse_pos):
		self.tiles.remove_tile(get_tile_from_pos(mouse_pos + self.scroll))

	def draw_mouse_rect(self, mouse_pos):
		if mouse_pos[1] < 500:
			tile_x, tile_y = get_tile_from_pos(mouse_pos + self.scroll)
			draw_rect(self.display, self.scroll, tile_x, tile_y)

	def draw_to_display(self, mouse_pos):
		self.display.fill((110, 110, 110))
		self.tiles.draw(self.display, self.scroll)
		self.draw_mouse_rect(mouse_pos)

	def draw(self, screen, mouse_pos):
		self.draw_to_display(mouse_pos)
		screen.blit(self.display, (0, 0))
