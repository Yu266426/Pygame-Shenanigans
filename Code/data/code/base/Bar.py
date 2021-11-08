import pygame

class Bar:
    def __init__(self, pos, size, backColour, fillColour):
        self.pos = pos

        self.size = size

        self.backColour = backColour

        self.fillColour = fillColour

        self.backRect = pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def draw(self, fillTotal, fillAmount, drawSurface):
        # Background
        pygame.draw.rect(drawSurface, self.backColour, self.backRect)

        # Fill
        fillRect = pygame.rect.Rect(self.pos[0] + 2, self.pos[1] + 2, self.size[0] * fillAmount / fillTotal - 4, self.size[1] - 4)
        pygame.draw.rect(drawSurface, self.fillColour, fillRect)