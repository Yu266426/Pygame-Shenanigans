import os

import pygame

from data.modules.file import TILE_DIR
from data.modules.settings import TILE_SIZE


def load_tile_image(folder_path, name):
	image = pygame.image.load(os.path.join(folder_path, name))
	return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))


def load_tile_images(tile_images):
	for directory_path, folders, file_names in os.walk(TILE_DIR):
		for folder in folders:
			if folder != "":
				temp_dict = {}

				folder_path = os.path.join(TILE_DIR, folder)
				for directory_path_2, folders_2, file_names_2 in os.walk(folder_path):
					for file in file_names_2:
						temp_dict[file[:-4]] = load_tile_image(folder_path, file)

				tile_images[folder] = temp_dict


TILE_IMAGES = {}
load_tile_images(TILE_IMAGES)
