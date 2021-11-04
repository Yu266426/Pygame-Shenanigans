import pygame
import os

from data.code.FileSetup import *

class Text:
    def __init__(self, x, y,  colour, size):
        self.x = x
        self.y = y

        self.colour = colour

        self.font = pygame.font.Font(os.path.join(DATA_FOLDER, "Moonrising.ttf"), size)

    # Draw From The Left    
    def drawLeft(self, text, drawSurface):
        textRendered = self.font.render(str(text), True, self.colour)
        drawSurface.blit(textRendered, (self.x, self.y)) 

    # Draw From The Center    
    def drawCentered(self, text, drawSurface):
        textRendered = self.font.render(str(text), True, self.colour)
        textRect = textRendered.get_rect()
        drawSurface.blit(textRendered, (self.x - (textRect.right - textRect.left) / 2, self.y)) 

    # Draw From The Right
    def drawRight(self, text, drawSurface):
        textRendered = self.font.render(str(text), True, self.colour)
        textRect = textRendered.get_rect()
        drawSurface.blit(textRendered, (self.x - (textRect.right - textRect.left), self.y)) 