import sys
import os

# File Setup
CURRENT_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0])) # Gets Current Path

DATA_FOLDER = os.path.join(CURRENT_FOLDER, "data") # Path For Data Folder

ASSET_FOLDER = os.path.join(DATA_FOLDER, "assets") # Path For Assets
AUDIO_FOLDER = os.path.join(DATA_FOLDER, "audio") # Path For Audio Folder
EXPLOSION_FOLDER = os.path.join(DATA_FOLDER, "explosions") # Path For Explosions Folder