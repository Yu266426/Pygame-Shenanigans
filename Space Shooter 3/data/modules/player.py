import pygame
import math
from data.modules.rotatable import Rotatable
from data.modules.images import PLAYER_IMAGE


class Player(Rotatable):
    def __init__(self, pos):
        super().__init__(pos, PLAYER_IMAGE)

        self.input = pygame.math.Vector2(0, 0)
        self.movement = pygame.math.Vector2(0, 0)

        self.acceleration = 1.3

        self.drag = 0.85

        # Laser
        self.is_firing = True

    # Gets WASD input
    def get_input(self):
        # Get keyboard input
        keys_pressed = pygame.key.get_pressed()

        if (keys_pressed[pygame.K_a] and keys_pressed[pygame.K_d]) or (keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_RIGHT]):
            self.input.x = 0
        elif keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.input.x = -1
        elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.input.x = 1
        else:
            self.input.x = 0

        if (keys_pressed[pygame.K_w] and keys_pressed[pygame.K_s]) or (keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_DOWN]):
            self.input.y = 0
        elif keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            self.input.y = -1
        elif keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            self.input.y = 1
        else:
            self.input.y = 0

        # Normalize
        if self.input.length() != 0:
            self.input.normalize_ip()

        # Get mouse input
        mouseInput = pygame.mouse.get_pressed(3)
        if mouseInput[0]:
            self.is_firing = True
        else:
            self.is_firing = False

    # Gets the relative angle to the mouse
    def get_angle_to_mouse(self, display_scale):
        mouse_pos = pygame.mouse.get_pos()

        # Gets the actual position on the screen, negates the difference in size of screen and display
        mouse_x = mouse_pos[0] - display_scale[0]/2
        mouse_y = mouse_pos[1] - display_scale[1]/2

        # Gets the relative angle
        self.angle = math.degrees(math.atan2(self.base_rect.centery - mouse_y, mouse_x - self.base_rect.centerx))

    # Moves the player
    def move(self, delta, scroll):
        # Get movement by adding onto previous, then applying drag
        self.movement += self.acceleration * delta * self.input
        self.movement *= self.drag

        # Moves the player, and gives offset for the rect
        self.pos += self.movement
        self.base_rect.center = self.pos - scroll

    # Runs all needed functions
    def update(self, delta, scroll, display_scale):
        self.get_input()

        self.move(delta, scroll)

        self.get_angle_to_mouse(display_scale)
        self.update_angle()
