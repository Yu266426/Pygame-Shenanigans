import json
import os.path

from data.modules.file import LEVEL_DIR
from data.modules.settings import TILE_SIZE, SCREEN_HEIGHT
from data.modules.tile import Tile


def read_from_json(name):
	"""
	Reads from a json file
	:param name: Name of file
	:return: dict
	"""
	json_path = os.path.join(LEVEL_DIR, f"{name}.json")
	with open(json_path) as file:
		data = file.read()

	return json.loads(data)


def initialize_list(size):
	"""
	Initializes a list with the given size
	:param size: (width, height)
	:return: list
	"""

	generated_list = []
	for row in range(size[1]):
		temp_list = []
		for column in range(size[0]):
			temp_list.append(None)
		generated_list.append(temp_list)

	return generated_list


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
	"""
	Returns the appropriate name for a tile given the surroundings
	:param type: Type of tile
	:param surroundings: (top, bottom, left, right, topleft, topright,  bottomleft, bottomright)
	:return: Name of tile
	"""

	name = type

	if not surroundings[1]:
		name += "_t"
	if not surroundings[0]:
		name += "_b"
	if not surroundings[2]:
		name += "_l"
	if not surroundings[3]:
		name += "_r"

	if not surroundings[6]:
		name += "_tl"
	if not surroundings[7]:
		name += "_tr"
	if not surroundings[4]:
		name += "_bl"
	if not surroundings[5]:
		name += "_br"

	return name


def get_tile_from_pos(pos):
	return round((pos[0] / TILE_SIZE) - 0.5), round((pos[1] / TILE_SIZE) - 0.5)


def get_tile(tile_pos, tile_list):
	if 0 <= tile_pos[1] < len(tile_list):
		if 0 <= tile_pos[0] < len(tile_list[tile_pos[1]]):
			return tile_list[tile_pos[1]][tile_pos[0]]


def check_tile(tile_pos, tile_list):
	if isinstance(get_tile(tile_pos, tile_list), Tile):
		return True
	return False
