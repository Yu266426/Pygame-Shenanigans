import random

import pygame

from Particle import Particle

pygame.init()

screen = pygame.display.set_mode((400, 300), pygame.SCALED)

clock = pygame.time.Clock()

rects = [pygame.rect.Rect(100, 200, 200, 30), pygame.rect.Rect(50, 250, 30, 200), pygame.rect.Rect(300, 50, 30, 100)]

particleList = []

running = True
while running:
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Background
	screen.fill((0, 0, 0))

	# Test environment
	for rect in rects:
		pygame.draw.rect(screen, (255, 255, 255), rect)

	# Mouse input
	mousePos = pygame.mouse.get_pos()
	mouseInput = pygame.mouse.get_pressed(3)

	if mouseInput[0]:
		for l in range(10):
			particleList.append(Particle(mousePos, (float(random.randint(-10, 10)) / 5.0, float(random.randint(-3, 3)) / 5.0), 3.0))

	# Particles
	for particle in particleList:
		particle.update(1, rects)
		particle.draw(screen)

	for particle in particleList:
		if particle.scale < 0:
			particleList.remove(particle)

	pygame.display.update()

pygame.quit()
