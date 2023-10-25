import pygame as pg
import random
import math


class Asteroid:
    def __init__(self, space, center, mu, sigma, maxr, num_points):
        self.space = space
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

    def update(self):
        pass

    def draw(self):
        pg.draw.polygon(self.space.game.screen, 'darkgray', self.points, 1)


class Space:
    def __init__(self, game, asteroids_number=50, asteroids_sizes=(5,25), asteroid_vertices=(5,15)):
        self.game = game
        self.asteroids = []
        self.asteroids_number = asteroids_number
        self.asteroids_sizes = asteroids_sizes
        self.asteroid_vertices = asteroid_vertices

    def generate_asteroids(self):
        for _ in range(self.asteroids_number):
            x = random.randint(0, self.game.screen_res[0])
            y = random.randint(0, self.game.screen_res[1])
            size = random.randint(*self.asteroids_sizes)
            vertices = random.randint(*self.asteroid_vertices)
            asteroid = Asteroid(self, (x, y), size, size / 4, size * 2, vertices)
            self.asteroids.append(asteroid)

    def update(self):
        for asteroid in self.asteroids:
            asteroid.update()

    def draw(self):
        for asteroid in self.asteroids:
            asteroid.draw()


class Game:
    def __init__(self, screen_res, fps):
        pg.init()
        self.screen_res = screen_res
        self.screen = pg.display.set_mode(self.screen_res)
        pg.display.set_caption("Asteroids")
        self.clock = pg.time.Clock()
        self.running = True
        self.fps = fps

        self.space = Space(self)
        self.space.generate_asteroids()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        self.space.update()
        self.clock.tick(self.fps)

    def draw(self):
        self.screen.fill('black')
        self.space.draw()
        pg.display.flip()

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        pg.quit()


if __name__ == '__main__':
    SCREEN_RES = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    FPS = 60
    game = Game(SCREEN_RES, FPS)
    game.run()
