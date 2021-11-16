import pygame
import random
import math


def get_movement(angle, speed):
    return pygame.math.Vector2(math.cos(math.radians(angle)) * speed, -1 * math.sin(math.radians(angle)) * speed)


def check_distance(pos1, pos2, distance):
    return math.dist(pos1, pos2) > distance


def get_random_float(range):
    return float(random.randint(range[0] * 20, range[1] * 20)) / 20
