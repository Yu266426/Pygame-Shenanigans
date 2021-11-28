from data.modules.helper import get_movement, check_distance
from data.modules.images import LASER_IMAGE
from data.modules.rotatable import Rotatable


class Laser(Rotatable):
	def __init__(self, pos, angle, origin):
		super().__init__(pos, LASER_IMAGE)

		self.angle = angle

		# (direction, speed)
		self.movement = get_movement(self.angle, 16)

		self.origin = origin

		self.angle_self()

		self.radius = 3

		self.damage = 5

	def move(self, delta, scroll):
		self.pos += self.movement * delta
		self.base_rect.center = self.pos - scroll

	def update(self, delta, scroll):
		self.move(delta, scroll)
		self.update_rect()

		if check_distance(self.pos, self.origin.pos, 1000):
			self.kill()
