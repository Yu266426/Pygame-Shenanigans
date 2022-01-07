import os
import shutil

import pygame

from data.modules.files import TILE_INPUT_DIR, GENERATED_TILES_DIR

# * Inputs
from data.modules.helper import swap_edge, swap_corner, generate_name

print()
print("Have 2 tiles as .png, one without any borders ({tilename}.png), and one with ({tilename}_bordered.png)")
tile_name = str.lower(input("Name of tile for generation: "))

tile = None
tile_bordered = None

try:
	tile = pygame.image.load(os.path.join(TILE_INPUT_DIR, f"{tile_name}.png"))
	tile_bordered = pygame.image.load(os.path.join(TILE_INPUT_DIR, f"{tile_name}_bordered.png"))
except FileNotFoundError:
	print(f"Could not find tile: {tile_name}")
	quit()

tile_height = tile.get_height()
tile_width = tile.get_width()

# * Generate Tiles
tile_outputs = {}

for sinp1 in range(0, 2):
	for sinp2 in range(0, 2):
		for sinp3 in range(0, 2):
			for sinp4 in range(0, 2):

				for cinp1 in range(0, 2):
					for cinp2 in range(0, 2):
						for cinp3 in range(0, 2):
							for cinp4 in range(0, 2):
								tile_outputs[
									generate_name(tile_name, (sinp1, sinp2, sinp3, sinp4, cinp1, cinp2, cinp3, cinp4))
								] = swap_corner((cinp1, cinp2, cinp3, cinp4), swap_edge((sinp1, sinp2, sinp3, sinp4), tile, tile_bordered), tile_bordered)

# * Save to pngs
OUTPUT_DIR = os.path.join(GENERATED_TILES_DIR, tile_name)

if os.path.exists(OUTPUT_DIR):
	shutil.rmtree(OUTPUT_DIR)

os.makedirs(OUTPUT_DIR)

for key in tile_outputs.keys():
	path = os.path.join(OUTPUT_DIR, f"{key}.png")
	pygame.image.save(tile_outputs[key], path)
