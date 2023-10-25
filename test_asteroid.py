import pygame as pg
import random
import math


SCREEN_RES = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
ASTEROIDS_NUMBER = 50
ASTEROIDS_SIZES = 5, 25
FPS = 60


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


pg.init()

screen = pg.display.set_mode(SCREEN_RES)
pg.display.set_caption("Asteroids")

asteroids = []

for i in range(ASTEROIDS_NUMBER):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    size = random.randint(*ASTEROIDS_SIZES)
    asteroid = generate_polygon((x, y), size, size / 4, size * 2, random.randint(5, 15))
    asteroids.append(asteroid)

clock = pg.time.Clock()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill('black')

    for asteroid in asteroids:
        pg.draw.polygon(screen, 'darkgray', asteroid, 1)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
