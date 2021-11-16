import pygame

from data.modules.files import PLAYER_IMAGE_PATH, LASER_IMAGE_PATH, LARGE_ASTEROID_IMAGE_PATH

PLAYER_IMAGE = pygame.image.load(PLAYER_IMAGE_PATH)
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (48, 48))

LASER_IMAGE = pygame.image.load(LASER_IMAGE_PATH)
LASER_IMAGE = pygame.transform.scale(LASER_IMAGE, (6 * 3.5, 6))

LARGE_ASTEROID_IMAGE = pygame.image.load(LARGE_ASTEROID_IMAGE_PATH)
LARGE_ASTEROID_IMAGE = pygame.transform.scale(LARGE_ASTEROID_IMAGE, (256, 256))
