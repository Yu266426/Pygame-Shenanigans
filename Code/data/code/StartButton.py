import pygame
import os
import math
import time

from pygame import mixer

from data.code.FileSetup import *
from data.code.Constants import *
from data.code.Settings import *

class StartButton:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.angle = 0
        self.selected = False

        self.scale = startButtonScale

        self.image = pygame.image.load(os.path.join(ASSET_FOLDER, "Start Button.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, startButtonScale)

        self.pressedSound = mixer.Sound(os.path.join(AUDIO_FOLDER, "Laser.wav"))
        self.pressedSound.set_volume(0.6 * volume)

        self.rect = self.image.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)
    
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

    # Draw Button
    def draw(self, drawSurface):
        rotatedImage = self.image

        # If selected, enlarge slightly
        if(self.selected == True):
            rotatedImage = pygame.transform.scale(rotatedImage, (int(self.scale * 2.3 * 1.1), int(self.scale * 1.1)))
        
        # Rotate The Image
        rotatedImage = pygame.transform.rotate(rotatedImage, self.angle * 5)
        newRect = rotatedImage.get_rect(center = self.image.get_rect(topleft = (self.x, self.y)).center)

        drawSurface.blit(rotatedImage, newRect)