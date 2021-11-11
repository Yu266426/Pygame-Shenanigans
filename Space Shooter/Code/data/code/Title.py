from data.code.base.Constants import *
from data.code.base.GameObject import GameObject
from data.code.base.Images import titleImage


class Title(GameObject):
    def __init__ (self, pos):
        super().__init__(pos, titleImage, titleScale)