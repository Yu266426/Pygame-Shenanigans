import pygame
import os

from data.modules.files import ASSET_FOLDER


class Text:
    def __init__(self, pos, colour, size, text=""):
        self.pos = pos

        self.colour = colour

        self.font = pygame.font.Font(os.path.join(ASSET_FOLDER, "Moonrising.ttf"), size)

        self.text = text

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def get_rect(self):
        text_temp = self.font.render(str(self.text), True, self.colour)
        return text_temp.get_rect()

    # Draw From The Left
    def draw_left(self, draw_surface):
        text_rendered = self.font.render(str(self.text), True, self.colour)
        draw_surface.blit(text_rendered, self.pos)

    # Draw From The Center
    def draw_centered(self, draw_surface):
        text_rendered = self.font.render(str(self.text), True, self.colour)
        text_rect = text_rendered.get_rect()
        draw_surface.blit(text_rendered, (self.pos[0] - (text_rect.right - text_rect.left) / 2, self.pos[1]))

    # Draw From The Right
    def draw_right(self, draw_surface):
        text_rendered = self.font.render(str(self.text), True, self.colour)
        text_rect = text_rendered.get_rect()
        draw_surface.blit(text_rendered, (self.pos[0] - (text_rect.right - text_rect.left), self.pos[1]))
