from data.modules.helper import tile_name_from_surroundings, initialize_list, get_tile_surroundings
from data.modules.tile import Tile


class TileList:
	def __init__(self, size, tiles):
		self.list = None
		self.parse_list(size, tiles)

	def parse_list(self, size, tiles):
		type_list = initialize_list(size)
		self.list = initialize_list(size)

		# Copy data to list
		for tile in tiles:
			pos = tile["pos"]
			type_list[pos[1]][pos[0]] = tile["type"]

		for row in range(len(type_list)):
			for column in range(len(type_list[row])):
				if type_list[row][column] is not None:
					self.list[row][column] = Tile((column, row), type_list[row][column], tile_name_from_surroundings(type_list[row][column], get_tile_surroundings((row, column), type_list)))

	def draw(self, display, scroll):
		for row in self.list:
			for tile in row:
				if isinstance(tile, Tile):
					tile.draw(display, scroll)
