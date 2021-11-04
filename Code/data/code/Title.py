from data.code.FileSetup import *
from data.code.Constants import *
from data.code.GameObject import GameObject

class Title(GameObject):
    def __init__ (self, pos):
        super().__init__(pos, os.path.join(ASSET_FOLDER, "Title.png"), titleScale)