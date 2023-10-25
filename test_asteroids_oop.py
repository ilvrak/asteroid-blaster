import pygame as pg
import random
import math


class Asteroid:
    def __init__(self, center, mu, sigma, maxr, num_points):
        self.center = center
        self.mu = mu
        self.sigma = sigma
        self.maxr = maxr
        self.num_points = num_points
        self.points = self.generate_polygon()

    def generate_polygon(self):
        def linspace(start, stop, num_steps):
            values = []
            delta = (stop - start) / num_steps
            for i in range(num_steps):
                values.append(start + i * delta)
            return values

        points = []
        for theta in linspace(0, 2 * math.pi - (2 * math.pi / self.num_points), self.num_points):
            radius = min(random.gauss(self.mu, self.sigma), self.maxr)
            x = self.center[0] + radius * math.cos(theta)
            y = self.center[1] + radius * math.sin(theta)
            points.append([x, y])
        return points


class Game:
    def __init__(self, screen_res, asteroids_number, asteroids_sizes, fps):
        pg.init()
        self.screen_res = screen_res
        self.screen = pg.display.set_mode(self.screen_res)
        pg.display.set_caption("Asteroids")
        self.clock = pg.time.Clock()
        self.running = True
        self.asteroids = []
        self.asteroids_number = asteroids_number
        self.asteroids_sizes = asteroids_sizes
        for _ in range(self.asteroids_number):
            x = random.randint(0, self.screen_res[0])
            y = random.randint(0, self.screen_res[1])
            size = random.randint(*self.asteroids_sizes)
            asteroid = Asteroid((x, y), size, size / 4, size * 2, random.randint(5, 15))
            self.asteroids.append(asteroid)
        self.fps = fps

    def run(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            self.screen.fill('black')

            for asteroid in self.asteroids:
                pg.draw.polygon(self.screen, 'darkgray', asteroid.points, 1)

            pg.display.flip()
            self.clock.tick(self.fps)

        pg.quit()


if __name__ == '__main__':
    SCREEN_RES = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    ASTEROIDS_NUMBER = 50
    ASTEROIDS_SIZES = 5, 25
    FPS = 60
    game = Game(SCREEN_RES, ASTEROIDS_NUMBER, ASTEROIDS_SIZES, FPS)
    game.run()
