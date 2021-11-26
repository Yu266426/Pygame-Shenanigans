import os
import sys

# * File paths
CURRENT_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))  # Gets Current Path

DATA_FOLDER = os.path.join(CURRENT_FOLDER, "data")  # Path For Data Folder

ASSET_FOLDER = os.path.join(DATA_FOLDER, "assets")  # Path For Assets
# AUDIO_FOLDER = os.path.join(DATA_FOLDER, "audio")  # Path For Audio Folder
# EXPLOSION_FOLDER = os.path.join(ASSET_FOLDER, "explosions")  # Path For Explosions Folder

# SETTINGS_FILE = os.path.join(DATA_FOLDER, "settings.json")

# * Image paths
PLAYER_IMAGE_PATH = os.path.join(ASSET_FOLDER, "player.png")

LASER_IMAGE_PATH = os.path.join(ASSET_FOLDER, "laser.png")

LARGE_ASTEROID_IMAGE_PATH = os.path.join(ASSET_FOLDER, "large asteroid.png")

MEDIUM_ASTEROID_IMAGE_PATH = os.path.join(ASSET_FOLDER, "medium asteroid.png")
