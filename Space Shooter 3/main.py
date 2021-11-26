import pygame

from data.modules.game import Game

pygame.init()

# Time
clock = pygame.time.Clock()

# Game
game = Game()

# ! FPS COUNTER (TEMP)
fps_counter = 0
fps_timer = 0

# Game loop
running = True
while running:
    # Limit framerate
    # clock.tick(60)

    # Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Run game update method
    game.update()

    # ! FPS TEMP
    fps_timer += game.delta / game.target_FPS
    fps_counter += 1
    if fps_timer > 1:
        fps_timer -= 1
        print(fps_counter)
        fps_counter = 0

    # Update display
    pygame.display.update()

pygame.quit()
