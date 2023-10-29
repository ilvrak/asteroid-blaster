import pygame as pg
import random
import math
import sys


class AsteroidBuilder:
    # create points array
    def __init__(self):
        self.linspace = None

    def gen_linspace(self):
        pass


class Asteroid(pg.sprite.Sprite):
    # position, size
    def __init__(self, space, center, mu, sigma, radius, num_points):
        super().__init__()
        self.space = space

        self.center = center
        self.x = center[0]
        self.y = center[1]
        self.mu = mu
        self.sigma = sigma
        self.radius = radius
        self.num_points = num_points
        self.points = self.generate_polygon()
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        self.image.fill('black')
        pg.draw.polygon(self.image, 'white', self.points)  # проблема здесь, координаты не подходят для этой поверхности
        self.image.set_colorkey('white')
        # self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def generate_polygon(self):
        def linspace(start, stop, num_steps):
            values = []
            delta = (stop - start) / num_steps
            for i in range(num_steps):
                values.append(start + i * delta)
            return values

        points = []
        for theta in linspace(0, 2 * math.pi - (2 * math.pi / self.num_points), self.num_points):
            point_radius = min(random.gauss(self.mu, self.sigma), self.radius)
            x = self.center[0] + point_radius * math.cos(theta)
            y = self.center[1] + point_radius * math.sin(theta)
            points.append([x, y])
        return points

    # def get_rect(self):
    #     return pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    # def get_mask(self):
    #     mask_surface = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
    #     pg.draw.polygon(mask_surface, (255, 255, 255), self.points)
    #     mask_surface.fill((255, 255, 255))
    #     mask_surface.set_colorkey((255, 255, 255))
    #     return pg.mask.from_surface(mask_surface)

    def update(self):
        pass

    def draw(self):
        if self.space.show_collide_rects:
            pg.draw.rect(self.space.game.screen, 'orchid4', self.rect, 1)
        if self.space.show_collide_masks:
            self.space.game.screen.blit(self.mask_image, self.rect)
        if self.space.show_objects:
            pg.draw.polygon(self.space.game.screen, 'darkgray', self.points, 1)

    def kill(self):
        pass


class Mouse(pg.sprite.Sprite):
    def __init__(self, space):
        super().__init__()
        self.space = space
        self.position = pg.mouse.get_pos()
        self.image = pg.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.color = 'red'
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def update(self):
        self.position = pg.mouse.get_pos()
        self.rect.topleft = self.position
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def draw(self):
        if self.space.show_collide_rects:
            pg.draw.rect(self.space.game.screen, 'magenta', self.rect, 1)
        if self.space.show_collide_masks:
            self.space.game.screen.blit(self.mask_image, self.position)
        if self.space.show_objects:
            self.space.game.screen.blit(self.image, self.position)
            self.image.fill(self.color)
            pg.draw.circle(self.image, 'white', (5, 5), 3, 1)


class Space:
    def __init__(self, game):
        self.game = game
        self.mouse = Mouse(self)
        self.asteroids = self.generate_asteroids()
        self.show_collide_rects = False
        self.show_collide_masks = False
        self.show_objects = True

    def generate_asteroids(self, asteroids_number=100, asteroids_sizes=(3, 10), asteroid_vertices=(5, 15)):
        asteroids = []
        for _ in range(asteroids_number):
            x = random.randint(0, self.game.screen_res[0])
            y = random.randint(0, self.game.screen_res[1])
            size = random.randint(*asteroids_sizes)
            vertices = random.randint(*asteroid_vertices)
            asteroid = Asteroid(self, (x, y), size, size / 4, size * 2, vertices)
            asteroids.append(asteroid)
        return asteroids

    def check_collision(self):
        collision_index = self.mouse.rect.collidelist([asteroid.rect for asteroid in self.asteroids])
        if collision_index == -1:
            self.mouse.color = 'green'
        else:
            self.mouse.color = 'red'

    def update(self):
        self.check_collision()
        self.mouse.update()
        for asteroid in self.asteroids:
            asteroid.update()

    def draw(self):
        self.mouse.draw()
        for asteroid in self.asteroids:
            asteroid.draw()


class Level:
    def __init__(self):
        pass


class Game:
    def __init__(self, screen_res, fps):
        pg.init()
        self.screen_res = screen_res
        self.screen = pg.display.set_mode(self.screen_res)
        pg.display.set_caption("Asteroids")
        self.clock = pg.time.Clock()
        self.running = True
        self.fps = fps
        pg.mouse.set_visible(False)
        self.space = Space(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.space.show_collide_rects = not self.space.show_collide_rects
                if event.key == pg.K_m:
                    self.space.show_collide_masks = not self.space.show_collide_masks
                if event.key == pg.K_o:
                    self.space.show_objects = not self.space.show_objects

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
        self.close()

    def close(self):
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    SCREEN_RES = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    FPS = 60
    game = Game(SCREEN_RES, FPS)
    game.run()
