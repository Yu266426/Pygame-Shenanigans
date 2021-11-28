import random

import pygame

from data.modules.game_object import GameObject
from data.modules.helper import get_random_float


class BackgroundStar(GameObject):
	def __init__(self, pos, size, bounds):
		# Premake image
		self.size = size

		self.grow_rate = get_random_float(-1, 1) * self.size / random.randint(90, 120)

		self.starting_size = self.size

		image = pygame.Surface((size, size))
		image.fill((255, 255, 255))

		super().__init__(pos, image)

		self.bounds = bounds

	def move(self, scroll):
		self.rect.center = self.pos - scroll * (self.starting_size / 10)

	def change_size(self, delta):
		if self.starting_size * 9 / 10 < self.size < self.starting_size * 11 / 10:
			self.size += self.grow_rate * delta
		else:
			self.grow_rate *= -1
			self.size += 2 * self.grow_rate * delta

		self.image = pygame.transform.scale(self.image, (self.size, self.size))
		self.rect = self.image.get_rect(center=self.rect.center)

	def update(self, delta, scroll, screen_size):
		self.move(scroll)
		self.change_size(delta)

		# Make stars loop
		if self.rect.center[0] >= screen_size[0] + 200:
			self.pos.x -= screen_size[0] + 200
		elif self.rect.center[0] <= -200:
			self.pos.x += screen_size[0] + 200

		if self.rect.center[1] >= screen_size[1] + 200:
			self.pos.y -= screen_size[0] + 200
		elif self.rect.center[1] <= -200:
			self.pos.y += screen_size[1] + 200
