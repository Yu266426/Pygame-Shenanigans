import pygame


class Bar:
    def __init__(self, pos, size, back_colour, fill_colour):
        self.pos = pos

        self.size = size

        self.backColour = back_colour

        self.fillColour = fill_colour

        self.backRect = pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def draw(self, fill_total, fill_amount, draw_surface):
        # Background
        pygame.draw.rect(draw_surface, self.backColour, self.backRect)

        # Fill
        fill_rect = pygame.rect.Rect(self.pos[0] + self.size[0] / 100, self.pos[1] + self.size[0] / 100, self.size[0] * fill_amount / fill_total - self.size[0] / 50, self.size[1] - self.size[0] / 50)
        pygame.draw.rect(draw_surface, self.fillColour, fill_rect)
