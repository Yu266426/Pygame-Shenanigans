import pygame

from data.code.base.Bar import Bar


def clamp(lowerBound, upperBound, num):
    if num < lowerBound:
        return lowerBound
    elif num > upperBound:
        return upperBound
    else:
        return num


class Slider(Bar):
    def __init__(self, pos, size, startingLevel):
        super().__init__(pos, size, (220, 220, 200), (255, 255, 255))

        self.selected = False

        self.fillAmount = startingLevel

    def update(self, mousePos, mouseInput):
        if pygame.Rect.collidepoint(self.backRect, mousePos[0], mousePos[1]):
            if mouseInput[0]:
                self.selected = True

        if self.selected:
            if mouseInput[0]:
                self.selected = False

            self.fillAmount = (clamp(self.pos[0], self.pos[0] + self.size[0], mousePos[0]) - self.pos[0]) / self.size[0]
