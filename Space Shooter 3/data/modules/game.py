import random
import time

import pygame
from pygame import mixer

from data.modules.background_stars import BackgroundStar
from data.modules.bar import Bar
from data.modules.explosion_particles import ExplosionParticle
from data.modules.files import LASER_FIRE_AUDIO_PATH, LASER_EXPLOSION_AUDIO_PATH, LARGE_ASTEROID_EXPLOSION_AUDIO_PATH, MEDIUM_ASTEROID_EXPLOSION_AUDIO_PATH, PLAYER_EXPLOSION_AUDIO_PATH
from data.modules.helper import get_random_float, get_angle_to, generate_offset, get_movement
from data.modules.images import PLAYER_IMAGE
from data.modules.large_asteroid import LargeAsteroid
from data.modules.laser import Laser
from data.modules.medium_asteroid import MediumAsteroid
from data.modules.player import Player
from data.modules.text import Text


class Game:
	def __init__(self):
		# * Screen setup
		self.screen = pygame.display.set_mode((800, 800))
		# Display for drawing on
		self.display = pygame.Surface((800, 800))
		pygame.display.set_caption("Space Shooter 3")
		pygame.display.set_icon(PLAYER_IMAGE)

		# FPS setup
		self.FPS = 60
		self.target_FPS = 60

		self.previous_time = time.time()
		self.delta = float(1)

		# * Game setup
		# Game state
		self.game_state = "game"

		# World
		self.scroll = pygame.math.Vector2(0, 0)
		self.offset_scroll = self.scroll
		self.follow_room = 15

		# * Objects
		# Star Field
		self.star_list = pygame.sprite.Group()
		self.generate_star_field((-200, -200), (self.display.get_width() + 200, self.display.get_height() + 200), 80)

		# Group Singles
		self.player = pygame.sprite.GroupSingle(Player((self.display.get_width() / 2, self.display.get_height() / 2)))

		# Groups
		self.laser_list = pygame.sprite.Group()
		self.asteroid_list = pygame.sprite.Group()
		self.explosion_list = pygame.sprite.Group()

		# * Cooldowns
		self.fire_countdown = 0
		self.asteroid_spawn_countdown = 0

		# * Progression
		self.asteroid_spawn_rate = float(200)

		# * Save data
		self.time_counter = 0
		self.player_pos = self.player.sprite.pos
		self.player_death_time = 0

		self.player_score = 0

		# * UI
		self.health_bar = Bar((20, 20), (250, 60), (50, 50, 50), (18, 161, 58))
		self.score_text = Text((780, 20), (200, 200, 200), 40)
		self.score_text.set_text(self.player_score)

		self.screen_shake = float(0)

		# * Audio
		self.laser_fire_sound = mixer.Sound(LASER_FIRE_AUDIO_PATH)
		self.laser_explosion_sound = mixer.Sound(LASER_EXPLOSION_AUDIO_PATH)
		self.large_asteroid_explosion_sound = mixer.Sound(LARGE_ASTEROID_EXPLOSION_AUDIO_PATH)
		self.medium_asteroid_explosion_sound = mixer.Sound(MEDIUM_ASTEROID_EXPLOSION_AUDIO_PATH)
		self.player_explosion_sound = mixer.Sound(PLAYER_EXPLOSION_AUDIO_PATH)

	# * Useful functions
	# Generate stars between two points
	def generate_star_field(self, p1, p2, star_count):
		for star in range(star_count):
			x = random.randint(p1[0], p2[0])
			y = random.randint(p1[1], p2[1])
			self.star_list.add(BackgroundStar((x, y), get_random_float(2, 6), abs(p1[0] - p2[0])))

	# Draw sprites visible
	def draw_group(self, group):
		for sprite in group.sprites():
			if sprite.rect.colliderect(self.display.get_rect()):
				self.display.blit(sprite.image, sprite.rect.topleft)

	# Returns the world scroll based on target
	def get_scroll(self, target):
		target_x = target.x - self.display.get_width() / 2
		target_y = target.y - self.display.get_height() / 2
		self.scroll += pygame.math.Vector2((target_x - self.scroll.x) / self.follow_room, (target_y - self.scroll.y) / self.follow_room) * self.delta
		if self.screen_shake != 0:
			self.offset_scroll.x = self.scroll.x + get_random_float(-8, 8)
			self.offset_scroll.y = self.scroll.y + get_random_float(-8, 8)

			self.screen_shake -= 1 * self.delta
			if self.screen_shake < 0:
				self.screen_shake = 0

	# * Spawners
	# Spawns laser, and handles cooldown
	def spawn_laser(self, spawner):
		if spawner is not None:
			if self.fire_countdown == 0 and spawner.is_firing:
				self.laser_fire_sound.play()
				self.laser_list.add(Laser(spawner.pos, spawner.angle, spawner))
				self.fire_countdown = float(8)
			else:
				if self.fire_countdown > 0:
					self.fire_countdown -= 1 * self.delta
				else:
					self.fire_countdown = 0

	# General spawners
	def spawn_asteroids(self):
		if self.asteroid_spawn_countdown == 0:
			for loop in range(random.randint(1, 3)):
				# Get target heading
				target_heading = pygame.math.Vector2(0, 0)

				# Get player direction
				if self.player.sprite is not None:
					target_heading.x = self.player.sprite.input.x
					target_heading.y = self.player.sprite.input.y

				# Offset from player
				if target_heading.length() == 0:
					# Player isn't moving, so comes from all angles
					offset = generate_offset(800)
				else:
					# Player moving, place in front so that they run into the asteroids
					offset = generate_offset(800, offset_direction=target_heading, angle_randomization=(-50, 50))

				spawn_position = self.player_pos + offset
				angle = get_angle_to(spawn_position, self.player_pos) + get_random_float(-10, 10)

				self.asteroid_list.add(LargeAsteroid(spawn_position, angle))

				# Add cooldown
				self.asteroid_spawn_countdown = float(self.asteroid_spawn_rate)
		else:
			if self.asteroid_spawn_countdown > 0:
				self.asteroid_spawn_countdown -= 1 * self.delta
			else:
				self.asteroid_spawn_countdown = 0

		self.asteroid_spawn_rate -= 0.03 * self.delta
		if self.asteroid_spawn_rate < 30:
			self.asteroid_spawn_rate = float(30)

	def spawn_explosion_particles(self, pos, count_range, spread, size_range, speed_range, decay_rate_range, type):
		for particle in range(random.randint(count_range[0], count_range[1])):
			# Generate offset to fill in the asteroid
			offset = generate_offset(get_random_float(0, spread))

			# Spawn particles
			self.explosion_list.add(ExplosionParticle(pos + offset, get_random_float(size_range[0], size_range[1]), get_random_float(speed_range[0], speed_range[1]), get_random_float(decay_rate_range[0], decay_rate_range[1]) / 30, type))

	# Explosion spawners
	def spawn_large_asteroid_explosion_particles(self, asteroid):
		self.spawn_explosion_particles(asteroid.pos, (200, 300), int(asteroid.image.get_width() / 2 - 20), (9, 15), (2, 4), (3, 6), "large_asteroid")

	def spawn_medium_asteroid_explosion_particles(self, asteroid):
		self.spawn_explosion_particles(asteroid.pos, (50, 100), int(asteroid.image.get_width() / 2 - 20), (8, 13), (2, 4), (5, 7), "medium_asteroid")

	def spawn_player_explosion_particles(self):
		for loop in range(3):
			self.spawn_explosion_particles(self.player.sprite.pos + generate_offset(30), (150, 200), int(self.player.sprite.image.get_width()), (8, 13), (3, 5), (4, 9), "player")

	# * Collisions
	def check_laser_asteroid_collision(self):
		collision_list = pygame.sprite.groupcollide(self.asteroid_list, self.laser_list, False, False, pygame.sprite.collide_circle)
		for asteroid in collision_list:
			# Get laser
			laser = collision_list[asteroid][0]

			asteroid.health -= laser.damage
			if asteroid.health <= 0:
				if isinstance(asteroid, LargeAsteroid):
					self.screen_shake = 10

					self.large_asteroid_explosion_sound.play()

					self.player_score += 20

					self.spawn_large_asteroid_explosion_particles(asteroid)

					# Spawn in the medium asteroids
					for medium_asteroid in range(random.randint(2, 4)):
						spawn_pos = asteroid.pos + generate_offset(get_random_float(0, asteroid.image.get_width() / 3))
						spawn_direction = asteroid.direction + get_random_float(-15, 15)
						self.asteroid_list.add(MediumAsteroid(spawn_pos, spawn_direction))

				elif isinstance(asteroid, MediumAsteroid):
					self.screen_shake = 4

					self.medium_asteroid_explosion_sound.play()

					self.player_score += 5

					self.spawn_medium_asteroid_explosion_particles(asteroid)

				asteroid.kill()

			self.laser_explosion_sound.play()
			self.spawn_explosion_particles(laser.pos, (5, 8), 3, (5, 7), (1, 2), (2, 3), "laser")
			laser.kill()

	def check_player_asteroid_collisions(self):
		collision_list = pygame.sprite.groupcollide(self.asteroid_list, self.player, False, False, pygame.sprite.collide_circle)
		for asteroid in collision_list:
			player = collision_list[asteroid][0]

			asteroid.health -= player.damage
			player.health -= asteroid.damage

			if asteroid.health <= 0:
				# Generate explosion particles
				if isinstance(asteroid, LargeAsteroid):
					self.screen_shake = 10

					self.large_asteroid_explosion_sound.play()

					self.spawn_large_asteroid_explosion_particles(asteroid)

					# Spawn in the medium asteroids
					for medium_asteroid in range(random.randint(2, 4)):
						spawn_pos = asteroid.pos + generate_offset(get_random_float(0, asteroid.image.get_width() / 3))
						spawn_direction = asteroid.direction + get_random_float(-15, 15)
						self.asteroid_list.add(MediumAsteroid(spawn_pos, spawn_direction))

				elif isinstance(asteroid, MediumAsteroid):
					self.screen_shake = 4

					self.medium_asteroid_explosion_sound.play()

					self.spawn_medium_asteroid_explosion_particles(asteroid)

				asteroid.kill()

			if player.health <= 0:
				self.screen_shake = 100
				self.player_explosion_sound.play()
				self.spawn_player_explosion_particles()
				player.kill()

	# * Game states
	# Testing state
	def game(self):
		# * Collisions
		self.check_laser_asteroid_collision()
		self.check_player_asteroid_collisions()

		# * Update
		self.star_list.update(self.delta, self.offset_scroll, self.display.get_size())

		self.player.update(self.delta, self.offset_scroll, self.display.get_width() / self.screen.get_width())
		if self.player.sprite is not None:
			self.spawn_explosion_particles(self.player.sprite.pos + get_movement(self.player.sprite.angle, -12), (1, 2), 3, (5, 8), (0, 1), (8, 14), "player_trail")

		self.spawn_laser(self.player.sprite)

		self.spawn_asteroids()

		self.laser_list.update(self.delta, self.offset_scroll)
		self.asteroid_list.update(self.delta, self.offset_scroll, self.player_pos, self.display.get_rect())

		# *  Particles
		self.explosion_list.update(self.delta, self.offset_scroll, self.player_pos)

		# * Draw
		self.draw_group(self.star_list)
		self.draw_group(self.asteroid_list)
		self.draw_group(self.laser_list)
		self.player.draw(self.display)
		self.draw_group(self.explosion_list)

		# * UI
		if self.player.sprite is not None:
			self.health_bar.draw(100, self.player.sprite.health, self.display)
		else:
			self.health_bar.draw(100, 0, self.display)

		self.score_text.set_text(self.player_score)
		self.score_text.draw_right(self.display)

		# * Death
		if self.player.sprite is None:
			if self.player_death_time == 0:
				self.player_death_time = self.time_counter
			elif self.time_counter - self.player_death_time > 6:
				self.game_state = "restart"

	# * Game loop
	def update(self):
		# * Gets delta time * targetFPS
		self.delta = (time.time() - self.previous_time)
		self.time_counter += self.delta
		self.delta *= self.target_FPS
		self.previous_time = time.time()

		# * Background
		self.display.fill((0, 0, 0))

		if self.player.sprite is not None:
			self.player_pos = self.player.sprite.pos
		self.get_scroll(self.player_pos)

		# * Game states
		if self.game_state == "game":
			self.game()

		if self.game_state == "restart":
			self.__init__()
			self.game_state = "game"

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
