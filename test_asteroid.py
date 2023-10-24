import pygame
import random
import math


ASTEROIDS_NUMBER = 50
ASTEROIDS_SIZES = 5, 25


def linspace(start, stop, num_steps):
    values = []
    delta = (stop - start) / num_steps
    for i in range(num_steps):
        values.append(start + i * delta)
    return values


def generate_polygon(center, mu, sigma, maxr, num_points):
    points = []

    for theta in linspace(0, 2 * math.pi - (2 * math.pi / num_points),
                          num_points):
        radius = min(random.gauss(mu, sigma), maxr)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append([x, y])

    return points


pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Asteroids")

polygons = []

for i in range(ASTEROIDS_NUMBER):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    size = random.randint(*ASTEROIDS_SIZES)
    polygon = generate_polygon((x, y), size, size / 4, size * 2, random.randint(5, 15))
    polygons.append(polygon)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for polygon in polygons:
        pygame.draw.polygon(screen, 'darkgray', polygon, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
