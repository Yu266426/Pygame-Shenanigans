import pygame

from data.modules.game import Game
from data.modules.settings import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
pygame.display.set_caption("Speed Run")

clock = pygame.time.Clock()

display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
game = Game(display)

# TODO: Flip the y axis, perhaps in post
running = True
while running:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

	display.fill((110, 110, 110))

	game.update(clock.get_time() / 1000 * 60)
	# game.update(1)

	screen.blit(pygame.transform.flip(display, False, True), (0, 0))
	pygame.display.update()
