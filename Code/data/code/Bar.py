import pygame

from pygame import Rect

class Bar:
    def __init__ (self, x, y, width, height, backColour, fillColour):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.backColour = backColour

        self.fillColour = fillColour

        self.backRect = Rect(self.x, self.y, self.width, self.height)

    def draw(self, fillTotal, fillAmount, drawSurface):
        # Background
        pygame.draw.rect(drawSurface, self.backColour, self.backRect)

        # Fill
        fillRect = Rect(self.x - 2 ,self.y + 2, self.width * fillAmount/fillTotal, self.height - 4)
        pygame.draw.rect(drawSurface, self.fillColour, fillRect)