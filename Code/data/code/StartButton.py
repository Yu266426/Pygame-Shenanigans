import pygame
import os
import math
import time

from pygame import mixer

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Settings import *
from data.code.Rotatable import Rotatable

class StartButton(Rotatable):
    def __init__(self, pos):
        super().__init__(pos, os.path.join(ASSET_FOLDER, "Start Button.png"), startButtonScale, 0)

        self.selected = False

        self.pressedSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser.wav"))
        self.pressedSound.set_volume(0.6 * volume)

    # Checks it mouse is over the button, and if it's pressed
    def check(self, mousePos, mouseState):
        # If mouse is over the button
        if(self.rect.collidepoint(mousePos)):
            self.angle = math.sin(time.time()*10)

            if(mouseState[0] == True):
                self.pressedSound.play()
                return True
        else:
            self.angle = 0
        
        return False

    # Rotate
    def rotate(self):
        # If selected, enlarge slightly
        if(self.selected == True):
            self.image = pygame.transform.scale(self.baseImage, (int(self.scale[0] * 1.1), int(self.scale[1] * 1.1)))
        else:
            self.image = self.baseImage.copy()
        
        # Rotate The Image
        self.image = pygame.transform.rotate(self.baseImage, self.angle * 5)
        self.rect = self.image.get_rect(center = self.baseImage.get_rect(topleft = (self.baseRect.x, self.baseRect.y)).center)