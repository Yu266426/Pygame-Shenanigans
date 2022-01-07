import os
import sys

CURRENT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

DATA_DIR = os.path.join(CURRENT_DIR, "data")

ASSET_DIR = os.path.join(DATA_DIR, "assets")

LEVEL_DIR = os.path.join(DATA_DIR, "levels")

TILE_DIR = os.path.join(ASSET_DIR, "tiles")
