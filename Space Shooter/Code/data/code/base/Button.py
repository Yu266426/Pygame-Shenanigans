import json
import math
import time

import pygame

from data.code.base.Constants import *
from data.code.base.FileSetup import *
from data.code.base.Rotatable import Rotatable

with open(SETTINGS_FILE) as file:
    settings = json.load(file)


class Button(Rotatable):
    def __init__(self, scale, image, pos, pressedSound, volume):
        super().__init__(pos, image, startButtonScale, 0)

        self.selected = False

        self.scale = scale

        self.pressedSound = pressedSound
        self.pressedSound.set_volume(volume * settings["volume"])

    # Checks it mouse is over the button, and if it's pressed
    def check(self, mousePos, mouseState):
        # If mouse is over the button
        if self.rect.collidepoint(mousePos):
            self.angle = math.sin(time.time() * 10)

            if mouseState[0]:
                self.pressedSound.play()
                return True
        else:
            self.angle = 0

        return False

    # Rotate
    def rotate(self):
        # If selected, enlarge slightly
        if self.selected:
            self.image = pygame.transform.scale(self.baseImage, (int(self.scale[1] * 1.1), int(self.scale[0] * 1.1)))
        else:
            self.image = self.baseImage.copy()

        # Rotate The Image
        self.image = pygame.transform.rotate(self.baseImage, self.angle * 5)
        self.rect = self.image.get_rect(center=self.baseImage.get_rect(topleft=(self.baseRect.x, self.baseRect.y)).center)
