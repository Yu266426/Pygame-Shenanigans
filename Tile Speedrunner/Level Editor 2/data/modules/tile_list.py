from data.modules.helper import tile_name_from_surroundings, initialize_list, get_tile_surroundings, in_bounds, copy_list, update_textures
from data.modules.tile import Tile


class TileList:
	def __init__(self, size, tiles):
		self.type_list = None
		self.list = None

		self.size = size

		self.parse_list(size, tiles)

	def parse_list(self, size, tiles):
		self.type_list = initialize_list(size)
		self.list = initialize_list(size)

		# Copy data to list
		for tile in tiles:
			pos = tile["pos"]
			self.type_list[pos[1]][pos[0]] = tile["type"]

		for row in range(len(self.type_list)):
			for column in range(len(self.type_list[row])):
				if self.type_list[row][column] is not None:
					self.list[row][column] = Tile((column, row), self.type_list[row][column], tile_name_from_surroundings(self.type_list[row][column], get_tile_surroundings((row, column), self.type_list)))

	def resize(self, size):
		new_type_list = initialize_list(size)
		copy_list(self.type_list, new_type_list)
		self.type_list = new_type_list

		new_list = initialize_list(size)
		copy_list(self.list, new_list)
		self.list = new_list

	def add_tile(self, pos, type):
		if pos[0] < 0 or pos[1] < 0:
			return

		# * Change size if needed
		size_changed = False
		if pos[1] >= len(self.type_list):
			self.size = (self.size[0], pos[1] + 1)
			size_changed = True
		if pos[0] >= len(self.type_list[0]):
			self.size = (pos[0] + 1, self.size[1])
			size_changed = True

		if size_changed:
			new_type_list = initialize_list(self.size)
			copy_list(self.type_list, new_type_list)
			self.type_list = new_type_list

			new_tile_list = initialize_list(self.size)
			copy_list(self.list, new_tile_list)
			self.list = new_tile_list

		# * Add tile
		self.type_list[pos[1]][pos[0]] = type

		# * Connect Textures
		update_textures(self.list, self.type_list, pos)

	def remove_tile(self, pos):
		if in_bounds(self.type_list, pos):
			self.type_list[pos[1]][pos[0]] = None
			self.list[pos[1]][pos[0]] = None

		update_textures(self.list, self.type_list, pos)

	def draw(self, display, scroll):
		for row in self.list:
			for tile in row:
				if isinstance(tile, Tile):
					tile.draw(display, scroll)
