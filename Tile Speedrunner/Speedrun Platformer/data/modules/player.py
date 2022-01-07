import pygame

from data.modules.helper import get_tile_from_pos, check_tile, get_tile
from data.modules.settings import TILE_SIZE, SCREEN_HEIGHT


class Player:
	def __init__(self, pos):
		self.pos = pygame.Vector2(pos[0], pos[1])

		self.spawn_point = pos

		self.image = pygame.Surface((TILE_SIZE * 0.7, TILE_SIZE * 1.6))
		self.image.fill((240, 110, 110))

		self.size = (self.image.get_width(), self.image.get_height())

		self.input = pygame.Vector2(0, 0)

		self.acceleration = 1
		self.drag = 0.87
		self.gravity = 0.8
		self.jump_height = 12

		self.movement = pygame.Vector2(0, 0)

		self.air_time = 100

	@property
	def rect(self):
		return pygame.Rect(self.pos[0] // 1, -(self.pos[1] // 1 - SCREEN_HEIGHT), self.size[0], self.size[1])

	def reset(self):
		self.pos.x = self.spawn_point[0]
		self.pos.y = self.spawn_point[1]

		self.movement.x = 0
		self.movement.y = 0

		self.air_time = 100

	def get_inputs(self):
		keys_pressed = pygame.key.get_pressed()

		if keys_pressed[pygame.K_a] and keys_pressed[pygame.K_d]:
			self.input.x = 0
		elif keys_pressed[pygame.K_a]:
			self.input.x = -1
		elif keys_pressed[pygame.K_d]:
			self.input.x = 1
		else:
			self.input.x = 0

		if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]:
			self.input.y = 0
		elif keys_pressed[pygame.K_w]:
			self.input.y = 1
		elif keys_pressed[pygame.K_s]:
			self.input.y = -1
		else:
			self.input.y = 0

	def move_x(self, delta):
		# More acceleration when switching directions
		if self.input.x != 0 and self.movement.x != 0:
			if self.input.x / self.input.x != self.movement.x / self.movement.x:
				self.acceleration = 3
			else:
				self.acceleration = 1
		else:
			self.acceleration = 1

		self.movement.x += self.input.x * self.acceleration
		self.movement.x *= self.drag

		self.pos.x += self.movement.x * delta

	def move_y(self, delta):
		# Jump
		if self.air_time <= 2 and self.input.y == 1:
			self.movement.y += self.jump_height
			self.air_time = 100

		# Gravity
		self.movement.y -= self.gravity * delta
		self.air_time += 1 * delta

		# Positions
		self.pos.y += self.movement.y * delta

	def check_colliding(self, tile_list, x):
		collide_list = []

		if check_tile(get_tile_from_pos(self.rect.topleft), tile_list):
			collide_list.append(get_tile(get_tile_from_pos(self.rect.topleft), tile_list))

		if check_tile(get_tile_from_pos(self.rect.midleft), tile_list):
			collide_list.append(get_tile(get_tile_from_pos(self.rect.midleft), tile_list))

		if check_tile(get_tile_from_pos((self.rect.bottomleft[0], self.rect.bottomleft[1] - 1)), tile_list):
			collide_list.append(get_tile(get_tile_from_pos((self.rect.bottomleft[0], self.rect.bottomleft[1] - 1)), tile_list))

		if check_tile(get_tile_from_pos((self.rect.topright[0] - 1, self.rect.topright[1])), tile_list):
			collide_list.append(get_tile(get_tile_from_pos((self.rect.topright[0] - 1, self.rect.topright[1])), tile_list))

		if check_tile(get_tile_from_pos((self.rect.midright[0] - 1, self.rect.midright[1])), tile_list):
			collide_list.append(get_tile(get_tile_from_pos((self.rect.midright[0] - 1, self.rect.midright[1])), tile_list))

		if check_tile(get_tile_from_pos((self.rect.bottomright[0] - 1, self.rect.bottomright[1] - 1)), tile_list):
			collide_list.append(get_tile(get_tile_from_pos((self.rect.bottomright[0] - 1, self.rect.bottomright[1] - 1)), tile_list))

		return collide_list

	def fix_x_collisions(self, tile_list):
		tiles = self.check_colliding(tile_list, True)
		for tile in tiles:
			if self.movement.x > 0:
				self.pos.x = tile.rect.left - self.rect.width

			elif self.movement.x < 0:
				self.pos.x = tile.rect.right

			self.movement.x = 0

	def fix_y_collisions(self, tile_list):
		tiles = self.check_colliding(tile_list, False)
		for tile in tiles:
			if self.movement.y < 0:
				self.pos.y = tile.rect.top - self.rect.height
				self.air_time = 0
			elif self.movement.y > 0:
				self.pos.y = tile.rect.bottom

			self.movement.y = 0

	def move(self, delta, tile_list):
		self.move_x(delta)
		self.fix_x_collisions(tile_list)

		self.move_y(delta)
		self.fix_y_collisions(tile_list)

		if self.pos.x < 0:
			self.pos.x = 0
			self.movement.x *= -1

		if self.pos.y < 0:
			self.reset()

	def update(self, delta, tile_list):
		print(f"({self.pos.x},{self.pos.y})")
		self.get_inputs()

		self.move(delta, tile_list)

	def draw(self, screen, scroll):
		screen.blit(self.image, self.rect.topleft - scroll)
