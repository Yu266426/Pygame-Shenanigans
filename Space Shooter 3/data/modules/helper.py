import math
import random

import pygame


def get_movement(angle, speed):
	return pygame.math.Vector2(math.cos(math.radians(angle)) * speed, -1 * math.sin(math.radians(angle)) * speed)


def check_distance(pos1, pos2, distance):
	return math.dist(pos1, pos2) > distance


def get_random_float(min, max):
	return float(random.randint(min * 30, max * 30)) / 30


def get_angle_to(pos1, pos2):
	# Gets the actual position on the screen, negates the difference in size of screen and display
	pos1_x = pos1[0]
	pos1_y = pos1[1]

	pos2_x = pos2[0]
	pos2_y = pos2[1]

	# Gets the relative angle
	return math.degrees(math.atan2(pos1_y - pos2_y, pos2_x - pos1_x))


def generate_offset(offset_amount, offset_direction=(1, 1), angle_randomization=(-180, 180)):
	offset = pygame.math.Vector2()
	offset.x = offset_direction[0]
	offset.y = offset_direction[1]

	if offset.length() != 0:
		offset.normalize_ip()

	offset.rotate_ip(get_random_float(angle_randomization[0], angle_randomization[1]))
	offset *= offset_amount

	return offset
