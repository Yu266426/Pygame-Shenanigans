import pygame
import random
import time

from data.modules.helper import get_random_float

from data.modules.player import Player
from data.modules.laser import Laser
from data.modules.large_asteroid import LargeAsteroid
from data.modules.background_stars import BackgroundStar
from data.modules.explosion_particles import ExplosionParticle


class Game:
    def __init__(self):
        # * Screen setup
        self.screen = pygame.display.set_mode((800, 800))
        # Display for drawing on
        self.display = pygame.Surface((800, 800))
        pygame.display.set_caption("Space Shooter 3")

        # FPS setup
        self.FPS = 60
        self.target_FPS = 60

        self.previous_time = time.time()
        self.delta = float(1)

        # * Game setup
        # Game state
        self.game_state = "test"

        # World
        self.scroll = pygame.math.Vector2(0, 0)
        self.follow_room = 25

        # * Objects
        # Star Field
        self.star_list = pygame.sprite.Group()
        self.generate_starfield((-200, -200), (1000, 1000), 80)

        # Group Singles
        self.player = pygame.sprite.GroupSingle(Player((self.display.get_width() / 2, self.display.get_height() / 2)))

        # Groups
        self.laser_list = pygame.sprite.Group()
        self.asteroid_list = pygame.sprite.Group()
        self.explosion_list = pygame.sprite.Group()

        # Cooldowns
        self.fire_countdown = 0

    # * Useful functions
    # Generate stars between two points
    def generate_starfield(self, p1, p2, star_count):
        for l in range(star_count):
            x = random.randint(p1[0], p2[0])
            y = random.randint(p1[1], p2[1])
            self.star_list.add(BackgroundStar((x, y), get_random_float((2, 6)), abs(p1[0] - p2[0])))

    # Draw sprites visible
    def draw_group(self, group):
        for sprite in group.sprites():
            if sprite.rect.colliderect(self.display.get_rect()):
                self.display.blit(sprite.image, sprite.rect.topleft)

    # Returns the world scroll based on target
    def get_scroll(self, target):
        target_x = target.x - self.display.get_width() / 2
        target_y = target.y - self.display.get_height() / 2
        self.scroll += pygame.math.Vector2((target_x - self.scroll.x) / self.follow_room * self.delta, (target_y - self.scroll.y) / self.follow_room * self.delta)

    # * Spawners
    # Spawns laser, and handles cooldown
    def spawn_laser(self, spawner):
        if self.fire_countdown == 0 and spawner.is_firing:
            self.laser_list.add(Laser(spawner.pos, spawner.angle, spawner))
            self.fire_countdown = float(10)
        else:
            if self.fire_countdown > 0:
                self.fire_countdown -= 1 * self.delta
            else:
                self.fire_countdown = 0

    # General spawner for asteroids
    def spawn_asteroids(self):
        pass

    # Spawn large asteroid
    def spawn_large_asteroid(self, pos, angle, speed):
        self.asteroid_list.add(LargeAsteroid(pos, angle, speed))

    # Spawn explosion particles in a given radius
    def spawn_explosion_particles(self, pos, count_range, spread, size_range, speed_range, decay_rate_range, type):
        for particle in range(random.randint(count_range[0], count_range[1])):
            # Generate offset to fill in the asteroid
            offset = pygame.math.Vector2(1, 1)
            offset.normalize_ip()
            offset.rotate_ip(random.randint(0, 360))
            offset *= random.randint(1, spread)

            # Spawn particles
            self.explosion_list.add(ExplosionParticle(pos + offset, get_random_float(size_range), get_random_float(speed_range), get_random_float(decay_rate_range)/30, type))

    # * Collisions
    def check_laser_asteroid_collision(self):
        collision_list = pygame.sprite.groupcollide(self.asteroid_list, self.laser_list, False, False, pygame.sprite.collide_circle)
        for asteroid in collision_list:
            for laser in collision_list[asteroid]:
                asteroid.health -= laser.damage

                if asteroid.health <= 0:
                    # Generate explosion particles
                    self.spawn_explosion_particles(asteroid.pos, (600, 650), int(asteroid.image.get_width()/2), (5, 9), (1, 3), (1, 3), "large_asteroid")
                    asteroid.kill()

                self.spawn_explosion_particles(laser.pos, (5, 8), 3, (5, 7), (1, 2), (2, 3), "laser")
                laser.kill()

    def check_player_asteroid_collisions(self):
        collision_list = pygame.sprite.groupcollide(self.player, self.asteroid_list, False, False, pygame.sprite.collide_circle)
        for player in collision_list:
            for asteroid in collision_list[player]:
                asteroid.health -= player.damage

                if asteroid.health <= 0:
                    # Generate explosion particles
                    self.spawn_explosion_particles(asteroid.pos, (600, 650), int(asteroid.image.get_width()/2 - 30), (5, 9), (1, 3), (1, 3), "large_asteroid")
                    asteroid.kill()

    # * Game states
    # Testing state
    def game(self):
        # * Update
        self.star_list.update(self.scroll, self.screen.get_size())

        self.player.update(self.delta, self.scroll, (self.screen.get_width() - self.display.get_width(), self.screen.get_height() - self.display.get_height()))

        self.spawn_laser(self.player.sprite)

        self.laser_list.update(self.delta, self.scroll)
        self.asteroid_list.update(self.delta, self.scroll, self.player.sprite)

        # * Collisions
        self.check_laser_asteroid_collision()
        self.check_player_asteroid_collisions()

        # *  Particles
        self.explosion_list.update(self.delta, self.scroll)

        # * Draw
        self.draw_group(self.star_list)
        self.draw_group(self.asteroid_list)
        self.draw_group(self.laser_list)
        self.player.draw(self.display)
        self.draw_group(self.explosion_list)

    # * Game loop
    def update(self):
        # Gets deltatime * targetFPS
        self.delta = (time.time() - self.previous_time) * self.target_FPS
        self.previous_time = time.time()

        # Background
        self.display.fill((0, 0, 0))

        self.get_scroll(self.player.sprite.pos)

        # Game states
        if self.game_state == "test":
            self.game()

        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
