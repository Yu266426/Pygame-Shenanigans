import os
import sys

# * File paths
CURRENT_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))  # Gets Current Path

DATA_FOLDER = os.path.join(CURRENT_FOLDER, "data")

ASSET_FOLDER = os.path.join(DATA_FOLDER, "assets")

AUDIO_FOLDER = os.path.join(DATA_FOLDER, "audio")

# * Image paths
PLAYER_IMAGE_PATH = os.path.join(ASSET_FOLDER, "player.png")

LASER_IMAGE_PATH = os.path.join(ASSET_FOLDER, "laser.png")

LARGE_ASTEROID_IMAGE_PATH = os.path.join(ASSET_FOLDER, "large asteroid.png")

MEDIUM_ASTEROID_IMAGE_PATH = os.path.join(ASSET_FOLDER, "medium asteroid.png")

# * Audio paths
LASER_FIRE_AUDIO_PATH = os.path.join(AUDIO_FOLDER, "laser fire.wav")

LASER_EXPLOSION_AUDIO_PATH = os.path.join(AUDIO_FOLDER, "laser explosion.wav")

LARGE_ASTEROID_EXPLOSION_AUDIO_PATH = os.path.join(AUDIO_FOLDER, "large asteroid explosion.wav")

MEDIUM_ASTEROID_EXPLOSION_AUDIO_PATH = os.path.join(AUDIO_FOLDER, "medium asteroid explosion.wav")

PLAYER_EXPLOSION_AUDIO_PATH = os.path.join(AUDIO_FOLDER, "player explosion.wav")
