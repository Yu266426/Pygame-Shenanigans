import json

import pygame

from data.modules.settings import TILE_SIZE, SCREEN_HEIGHT
from data.modules.tile import Tile


def read_from_json(path):
	with open(path) as file:
		data = file.read()

	return json.loads(data)


def tile_for_json(tile, pos):
	tile_dict = {
		"type": tile.type,
		"pos": [pos[1], pos[0]]
	}

	return tile_dict


def initialize_list(size):
	generated_list = []
	if size[0] == 0 and size[1] == 0:
		return [[]]
	elif size[0] == 1 and size[1] == 0:
		return [[None]]

	for row in range(size[1]):
		temp_list = []
		for column in range(size[0]):
			temp_list.append(None)
		generated_list.append(temp_list)

	return generated_list


def copy_list(input_list, output_list):
	for row in range(min(len(input_list), len(output_list))):
		for column in range(min(len(input_list[row]), len(output_list[row]))):
			output_list[row][column] = input_list[row][column]


def in_bounds(check_list, index):
	if 0 <= index[0] < len(check_list[0]):
		if 0 <= index[1] < len(check_list):
			return True

	return False


def get_tile_surroundings(pos, type_list):
	surroundings = [False, False, False, False, False, False, False, False]

	row = pos[0]
	column = pos[1]

	# Top
	if row + 1 < len(type_list):
		if type_list[row + 1][column] == type_list[row][column]:
			surroundings[0] = True

	# Bottom
	if 0 <= row - 1:
		if type_list[row - 1][column] == type_list[row][column]:
			surroundings[1] = True

	# Left
	if 0 <= column - 1:
		if type_list[row][column - 1] == type_list[row][column]:
			surroundings[2] = True

	# Right
	if column + 1 < len(type_list[row]):
		if type_list[row][column + 1] == type_list[row][column]:
			surroundings[3] = True

	# Topleft
	if row + 1 < len(type_list) and 0 <= column - 1:
		if type_list[row + 1][column - 1] == type_list[row][column]:
			surroundings[4] = True

	# Topright
	if row + 1 < len(type_list) and column + 1 < len(type_list[row]):
		if type_list[row + 1][column + 1] == type_list[row][column]:
			surroundings[5] = True

	# Bottomleft
	if 0 <= row - 1 and 0 <= column - 1:
		if type_list[row - 1][column - 1] == type_list[row][column]:
			surroundings[6] = True

	# Bottomright
	if 0 <= row - 1 and column + 1 < len(type_list[row]):
		if type_list[row - 1][column + 1] == type_list[row][column]:
			surroundings[7] = True

	return surroundings


def tile_name_from_surroundings(type, surroundings):
	name = type

	if not surroundings[0]:
		name += "_t"
	if not surroundings[1]:
		name += "_b"
	if not surroundings[2]:
		name += "_l"
	if not surroundings[3]:
		name += "_r"

	if not surroundings[4]:
		name += "_tl"
	if not surroundings[5]:
		name += "_tr"
	if not surroundings[6]:
		name += "_bl"
	if not surroundings[7]:
		name += "_br"

	return name


def get_tile_from_pos(pos):
	return round((pos[0] / TILE_SIZE) - 0.5), round(((SCREEN_HEIGHT - pos[1]) / TILE_SIZE) - 0.5)


def get_tile(tile_pos, tile_list):
	if 0 <= tile_pos[1] < len(tile_list):
		if 0 <= tile_pos[0] < len(tile_list[tile_pos[1]]):
			return tile_list[tile_pos[1]][tile_pos[0]]


def update_textures(tile_list, type_list, pos):
	for x in range(-1, 2):
		if 0 <= pos[0] + x < len(type_list[0]):
			for y in range(-1, 2):
				if 0 <= pos[1] + y < len(type_list):
					if type_list[pos[1] + y][pos[0] + x] is not None:
						tile_list[pos[1] + y][pos[0] + x] = Tile((pos[0] + x, pos[1] + y), type_list[pos[1] + y][pos[0] + x], tile_name_from_surroundings(type_list[pos[1] + y][pos[0] + x], get_tile_surroundings((pos[1] + y, pos[0] + x), type_list)))


def draw_rect(screen, scroll, tile_x, tile_y, colour=(200, 0, 0), stroke_size=1, tile_size=TILE_SIZE):
	pygame.draw.rect(screen, colour, (tile_x * tile_size - scroll.x, ((screen.get_height() / tile_size) - tile_y - 1) * tile_size - scroll.y, tile_size, tile_size), stroke_size)
