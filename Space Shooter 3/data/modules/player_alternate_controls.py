import pygame

from data.modules.images import PLAYER_IMAGE
from data.modules.rotatable import Rotatable


class Player(Rotatable):
	def __init__(self, pos):
		super().__init__(pos, PLAYER_IMAGE)

		self.input = pygame.math.Vector2(0, 0)
		self.movement = pygame.math.Vector2(0, 0)
		self.acceleration = 1.3
		self.drag = 0.85

		self.turn_input = 0
		self.turn_movement = 0
		self.turn_acceleration = 0.9
		self.turn_drag = 0.9

		# Laser
		self.is_firing = False

		# Collision
		self.radius = PLAYER_IMAGE.get_width() / 2 - 3

		self.max_health = 100
		self.health = self.max_health
		self.damage = self.health

	# Gets input
	def get_input(self):
		# Get keyboard input
		keys_pressed = pygame.key.get_pressed()

		if keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_RIGHT]:
			self.turn_input = 0
		elif keys_pressed[pygame.K_LEFT]:
			self.turn_input = 1
		elif keys_pressed[pygame.K_RIGHT]:
			self.turn_input = -1
		else:
			self.turn_input = 0

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
			self.input.y = -1
		elif keys_pressed[pygame.K_s]:
			self.input.y = 1
		else:
			self.input.y = 0

		# Get mouse input
		if keys_pressed[pygame.K_SPACE]:
			self.is_firing = True
		else:
			self.is_firing = False

	# Moves the player
	def move(self, delta, scroll):
		# Get movement by adding onto previous, then applying drag
		self.movement += self.acceleration * self.input
		self.movement *= self.drag

		self.turn_movement += self.turn_acceleration * self.turn_input
		self.turn_movement *= self.turn_drag

		# Moves the player, and gives offset for the rect
		# Angles player
		self.pos += self.movement * delta
		self.base_rect.center = self.pos - scroll

		self.angle += self.turn_movement * delta

	# Runs all needed functions
	def update(self, delta, scroll, display_ratio):
		self.get_input()

		self.move(delta, scroll)

		self.update_angle()
