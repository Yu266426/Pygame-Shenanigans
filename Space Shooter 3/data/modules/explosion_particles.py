import random

import pygame

from data.modules.game_object import GameObject
from data.modules.helper import get_random_float, check_distance

colour_palette = {
	"large_asteroid": [(235, 143, 30), (235, 62, 14), (255, 208, 54)],
	"medium_asteroid": [(240, 109, 23), (246, 143, 35), (245, 162, 25)],
	"laser": [(252, 207, 3), (255, 248, 43), (255, 166, 0)],
	"player": [(235, 143, 30), (235, 62, 14), (255, 208, 54), (240, 109, 23), (246, 143, 35), (245, 162, 25), (252, 207, 3), (255, 248, 43), (255, 166, 0)],
	"player_trail": [(3, 232, 252), (32, 179, 247), (0, 226, 230)],
	"fireball": [(235, 143, 30), (235, 62, 14), (255, 208, 54), (240, 109, 23), (246, 143, 35), (245, 162, 25), (252, 207, 3), (255, 248, 43), (255, 166, 0)]
}


class ExplosionParticle(GameObject):
	def __init__(self, pos, scale, speed, decay_rate, particle_type):
		# Make image to pass into initialization
		image = pygame.Surface((scale, scale))
		image.fill(random.choice(colour_palette[particle_type]))

		# Initialize
		super().__init__(pos, image)

		self.scale = float(scale)
		self.decay_rate = decay_rate

		self.movement = pygame.math.Vector2(1, 1)
		self.movement.normalize_ip()
		self.movement *= speed
		self.movement.rotate_ip(get_random_float(0, 360))

	def move(self, delta, scroll):
		# Move
		self.pos += self.movement * delta

		# Change angle slightly
		self.movement.rotate_ip(get_random_float(-6, 6))

		self.scale -= self.decay_rate * delta

		if self.scale > 0:
			self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
			self.rect = self.image.get_rect()
			self.rect.center = self.pos - scroll

	def collision(self, player_pos):
		if not check_distance(self.pos, player_pos, 25):
			speed = self.movement.length()
			self.movement = self.pos - player_pos
			if self.movement.length() != 0:
				self.movement.normalize_ip()
			self.movement *= speed

	def update(self, delta, scroll, player_pos):
		self.move(delta, scroll)

		# Have it bounce off player
		self.collision(player_pos)

		if self.scale <= 2:
			self.kill()
