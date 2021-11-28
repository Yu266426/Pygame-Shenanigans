import pygame

from data.modules.helper import get_angle_to
from data.modules.images import PLAYER_IMAGE
from data.modules.rotatable import Rotatable


class Player(Rotatable):
	def __init__(self, pos):
		super().__init__(pos, PLAYER_IMAGE)

		self.input = pygame.math.Vector2(0, 0)
		self.movement = pygame.math.Vector2(0, 0)

		self.acceleration = 1.3

		self.drag = 0.85

		# Laser
		self.is_firing = True

		# Collision
		self.radius = PLAYER_IMAGE.get_width() / 2

		self.health = 100
		self.damage = self.health

	# Gets WASD input
	def get_input(self):
		# Get keyboard input
		keys_pressed = pygame.key.get_pressed()

		if (keys_pressed[pygame.K_a] and keys_pressed[pygame.K_d]) or (keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_RIGHT]):
			self.input.x = 0
		elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
			self.input.x = -1
		elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
			self.input.x = 1
		else:
			self.input.x = 0

		if (keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]) or (keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_DOWN]):
			self.input.y = 0
		elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
			self.input.y = -1
		elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
			self.input.y = 1
		else:
			self.input.y = 0

		# Normalize
		if self.input.length() != 0:
			self.input.normalize_ip()

		# Get mouse input
		mouse_input = pygame.mouse.get_pressed(3)
		if mouse_input[0]:
			self.is_firing = True
		else:
			self.is_firing = False

	# Gets the relative angle to the mouse
	def get_angle_to_mouse(self, display_ratio):
		mouse_pos = pygame.mouse.get_pos()

		relative_mouse_x = mouse_pos[0] * display_ratio
		relative_mouse_y = mouse_pos[1] * display_ratio

		self.angle = get_angle_to(self.rect.center, (relative_mouse_x, relative_mouse_y))

	# Moves the player
	def move(self, delta, scroll):
		# Get movement by adding onto previous, then applying drag
		self.movement += self.acceleration * self.input
		self.movement *= self.drag

		# Moves the player, and gives offset for the rect
		self.pos += self.movement * delta
		self.base_rect.center = self.pos - scroll

	# Runs all needed functions
	def update(self, delta, scroll, display_ratio):
		self.get_input()

		self.move(delta, scroll)

		self.get_angle_to_mouse(display_ratio)
		self.update_angle()
