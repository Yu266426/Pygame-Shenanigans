def swap(start_pos, end_pos, starting_tile, swap_tile):
	new_tile = starting_tile.copy()

	for column in range(start_pos[0], end_pos[0]):
		for row in range(start_pos[1], end_pos[1]):
			new_tile.set_at((column, row), swap_tile.get_at((column, row)))

	return new_tile


def swap_edge(edges, starting_tile, swap_tile):
	# edges -> (top, bottom, left, right)
	new_tile = starting_tile.copy()

	if edges[0]:
		new_tile = swap((0, 0), (new_tile.get_width(), 1), new_tile, swap_tile)

	if edges[1]:
		new_tile = swap((0, new_tile.get_height() - 1), (new_tile.get_width(), new_tile.get_height()), new_tile, swap_tile)

	if edges[2]:
		new_tile = swap((0, 0), (1, new_tile.get_height()), new_tile, swap_tile)

	if edges[3]:
		new_tile = swap((new_tile.get_width() - 1, 0), (new_tile.get_width(), new_tile.get_height()), new_tile, swap_tile)

	return new_tile


def swap_corner(corner, starting_tile, swap_tile):
	"""

	:param corner: (topleft, topright, bottomleft, bottomright)
	"""
	new_tile = starting_tile.copy()

	if corner[0]:
		new_tile.set_at((0, 0), swap_tile.get_at((0, 0)))
	if corner[1]:
		new_tile.set_at((new_tile.get_width() - 1, 0), swap_tile.get_at((new_tile.get_width() - 1, 0)))
	if corner[2]:
		new_tile.set_at((0, new_tile.get_height() - 1), swap_tile.get_at((0, new_tile.get_height() - 1)))
	if corner[3]:
		new_tile.set_at((new_tile.get_width() - 1, new_tile.get_height() - 1), swap_tile.get_at((new_tile.get_width() - 1, new_tile.get_height() - 1)))

	return new_tile


def generate_name(tile_name, surroundings):
	"""
	:param surroundings: (top, bottom, left, right, topleft, topright,  bottomleft, bottomright)
	:return: str
	"""
	name = tile_name

	if surroundings[0]:
		name += "_t"
	if surroundings[1]:
		name += "_b"
	if surroundings[2]:
		name += "_l"
	if surroundings[3]:
		name += "_r"

	if surroundings[4]:
		name += "_tl"
	if surroundings[5]:
		name += "_tr"
	if surroundings[6]:
		name += "_bl"
	if surroundings[7]:
		name += "_br"

	return name
