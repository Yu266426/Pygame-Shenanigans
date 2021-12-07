import random

import pygame

from data.modules.explosion_particles import ExplosionParticle
from data.modules.game_object import GameObject
from data.modules.helper import get_movement, get_random_float, generate_offset


class FireBall(GameObject):
	def __init__(self, pos, direction, speed, size, explosion_list):
		image = pygame.Surface((size, size))

		super().__init__(pos, image)

		self.movement = get_movement(direction, speed)

		self.radius = size

		self.damage = 5

		self.explosion_list = explosion_list

	def move(self, delta, scroll):
		self.pos += self.movement * delta
		self.rect.center = self.pos - scroll

	def update(self, delta, scroll, display):
		self.move(delta, scroll)

		self.radius -= 0.1 * delta

		if self.radius > 1:
			# Only make effects in view
			if self.rect.colliderect(display):
				upper_bound = int(self.radius / 2)
				if upper_bound < 6:
					upper_bound = 6

				for spark in range(random.randint(5, upper_bound)):
					self.explosion_list.add(ExplosionParticle(self.pos + generate_offset(get_random_float(0, int(self.radius + 5))), get_random_float(9, 15), get_random_float(2, 4), get_random_float(1, 3), "fireball"))
		else:
			self.kill()
