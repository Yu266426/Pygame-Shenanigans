import json
import os.path

import pygame

from data.modules.files import LEVEL_DIR
from data.modules.helper import read_from_json, tile_for_json
from data.modules.images import ICON_IMAGE
from data.modules.level import Level
from data.modules.selector import Selector

level_name = input("Input the level name: ")
file_name = f"{level_name}.json"
file_path = os.path.join(LEVEL_DIR, file_name)

# * Create Folder
if not os.path.isfile(file_path):
	print("Level does not exists. Do you want to create a new level?")

	user_response = input("Y for yes / N for no: ").lower()

	if user_response == "y":
		with open(file_path, "x") as file:
			print(f"Creating: {file.name} at {file_path}")

		data_json = {"width": 1, "height": 1, "tiles": []}
		with open(file_path, "w") as file:
			file.write(json.dumps(data_json))

	else:
		quit(0)


# * Functions
def save():
	print(f"Saving file {file_name} at {file_path}...")

	# Update information
	level_data = read_from_json(file_path)

	level_data["tiles"] = []

	width = 0
	height = 0
	for row in range(len(level.tiles.list)):
		for column in range(len(level.tiles.list[row])):
			tile = level.tiles.list[row][column]
			if tile is not None:
				if row > height:
					height = row
				if column > width:
					width = column
				level_data["tiles"].append(tile_for_json(tile, (row, column)))

	level_data["height"] = height + 1
	level_data["width"] = width + 1

	level.tiles.resize((width + 1, height + 1))

	# Write to file
	with open(file_path, "w") as write_file:
		write_file.write(json.dumps(level_data))

	print("File saved")


# * Editor
pygame.init()

screen = pygame.display.set_mode((800, 700))
caption = f"Level Editor 2: {level_name}"
pygame.display.set_caption(caption)
pygame.display.set_icon(ICON_IMAGE)

clock = pygame.time.Clock()

#  TODO: Add support for positioning player
level = Level(file_path)

selector = Selector()

edited = False
running = True
while running:
	clock.tick()
	delta = clock.get_time() / 1000 * 60

	mouse_pos = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed(3)
	mouse_wheel = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

			if event.key == pygame.K_s:
				save()
				edited = False

		if event.type == pygame.MOUSEWHEEL:
			mouse_wheel = event.y

	# * Editing
	# In level
	if mouse_pos[1] < 500:
		# Editing
		if mouse_pressed[0]:
			level.add_tile(mouse_pos, selector.selected_tile)
			edited = True
		if mouse_pressed[2]:
			level.remove_tile(mouse_pos)
			edited = True

		# Movement
		level.move(mouse_pressed[1], mouse_pos)

	# In editor
	else:
		if mouse_pressed[0]:
			selector.select_tile(mouse_pos)

	# * Draw
	level.draw(screen, mouse_pos)

	selector.draw(screen)

	pygame.display.update()

	# * Caption
	if not edited:
		pygame.display.set_caption(caption)
	else:
		pygame.display.set_caption(f"{caption}*")

# * Save
if edited:
	save()

pygame.quit()
