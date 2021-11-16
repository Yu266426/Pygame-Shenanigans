import pygame

from data.modules.game import Game

pygame.init()

# Time
clock = pygame.time.Clock()

# Game
game = Game()

# Game loop
running = True
while running:
    # Limit framerate
    clock.tick(60)

    # Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                game.spawn_large_asteroid((200, 200), 45, (2, 5))

    # Run game update method
    game.update()

    # Update display
    pygame.display.update()

pygame.quit()
