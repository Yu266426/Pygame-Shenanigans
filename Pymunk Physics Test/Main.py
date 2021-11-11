import pygame
import pymunk

pygame.init()


def createCircle(space, pos):
    # Body that is moved
    body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
    body.position = pos

    # Shape for collisions
    shape = pymunk.Circle(body, 30)

    # Add object to space
    space.add(body, shape)

    return shape


def drawCircles(circles):
    for circle in circles:
        pygame.draw.circle(screen, (0, 0, 0), circle.body.position, 30)


def createStaticCircles(space, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)

    body.position = pos

    shape = pymunk.Circle(body, 20)

    space.add(body, shape)

    return shape


def drawStaticCircles(circles):
    for circle in circles:
        pygame.draw.circle(screen, (0, 0, 0), circle.body.position, 20)


# Pygame
screen = pygame.display.set_mode((400, 300), pygame.SCALED)

clock = pygame.time.Clock()

# Pymunk
# The domain of the physics sim
space = pymunk.Space()
# Horizontal gravity, vertical gravity
space.gravity = (0, 500)

circleList = []


staticCirleList = []
staticCirleList.append(createStaticCircles(space, (230, 200)))
staticCirleList.append(createStaticCircles(space, (170, 240)))

running = True
while running:
    clock.tick(60)

    screen.fill((100, 100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            circleList.append(createCircle(space, event.pos))

    # Update physics
    space.step(1 / 50)

    # Draw
    drawCircles(circleList)

    drawStaticCircles(staticCirleList)

    for circle in circleList:
        if circle.body.position[1] > screen.get_size()[1] + 100:
            circleList.remove(circle)

    # Update Screen
    pygame.display.update()

pygame.quit()
