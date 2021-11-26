import os
import sys

# * File paths
CURRENT_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))  # Gets Current Path

DATA_FOLDER = os.path.join(CURRENT_FOLDER, "data")  # Path For Data Folder

ASSET_FOLDER = os.path.join(DATA_FOLDER, "assets")  # Path For Assets

# * Image paths
PLAYER_IMAGE_PATH = os.path.join(ASSET_FOLDER, "player.png")

LASER_IMAGE_PATH = os.path.join(ASSET_FOLDER, "laser.png")

LARGE_ASTEROID_IMAGE_PATH = os.path.join(ASSET_FOLDER, "large asteroid.png")

MEDIUM_ASTEROID_IMAGE_PATH = os.path.join(ASSET_FOLDER, "medium asteroid.png")
