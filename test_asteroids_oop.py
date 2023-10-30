import pygame as pg
import random
import math
import sys


class Asteroid(pg.sprite.Sprite):
    def __init__(self, space, center):
        super().__init__()
        self.space = space

        self.center = center
        self.points = self.build_polygon()
        min_x, min_y = map(min, zip(*self.points))
        max_x, max_y = map(max, zip(*self.points))
        width = max_x - min_x + 3
        height = max_y - min_y + 3
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.width = width
        self.rect.height = height
        pg.draw.polygon(self.image, 'darkgray', [(x - min_x + 1, y - min_y + 1) for x, y in self.points])
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.image.fill(pg.SRCALPHA)
        pg.draw.polygon(self.image, 'darkgray', [(x - min_x + 1, y - min_y + 1) for x, y in self.points], 1)

    def build_polygon(self):
        mean = random.randint(30, 30)
        deviation = mean / 4
        radius = mean * 2
        vertices = random.randint(5, 15)
        angles = [i * 2 * math.pi / vertices for i in range(vertices)]

        polygon = []
        for angle in angles:
            rib_radius = min(random.gauss(mean, deviation), radius)
            x = self.center[0] + rib_radius * math.cos(angle)
            y = self.center[1] + rib_radius * math.sin(angle)
            polygon.append( (int(x), int(y)) )
        print(polygon)
        return polygon

    def update(self):
        pass
        # self.mask = pg.mask.from_surface(self.image)
        # self.mask_image = self.mask.to_surface()

    def draw(self):
        if self.space.show_collide_rects:
            pg.draw.rect(self.space.game.screen, 'darkmagenta', self.rect, 1)
        if self.space.show_collide_masks:
            self.space.game.screen.blit(self.mask_image, self.rect)
        if self.space.show_objects:
            # pg.draw.polygon(self.space.game.screen, 'darkgray', self.points, 1)
            self.space.game.screen.blit(self.image, self.rect)


class Mouse(pg.sprite.Sprite):
    def __init__(self, space):
        super().__init__()
        self.space = space
        self.position = pg.mouse.get_pos()
        self.image = pg.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.color = 'red'
        self.mask = pg.mask.from_surface(self.image)

    def check_collision(self):
        if pg.sprite.spritecollide(self, self.space.asteroids, False):
            self.color = 'blue'
            if pg.sprite.spritecollide(self, self.space.asteroids, False, pg.sprite.collide_mask):
                self.color = 'red'
        else:
            self.color = 'green'

    def update(self):
        self.position = pg.mouse.get_pos()
        self.rect.topleft = self.position
        self.check_collision()
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def draw(self):
        if self.space.show_collide_rects:
            pg.draw.rect(self.space.game.screen, 'darkmagenta', self.rect, 1)
        if self.space.show_collide_masks:
            self.space.game.screen.blit(self.mask_image, self.rect)
        if self.space.show_objects:
            self.space.game.screen.blit(self.image, self.position)
            self.image.fill(self.color)


class Space:
    def __init__(self, game):
        self.game = game
        self.mouse = Mouse(self)
        self.asteroids = self.generate_asteroids()
        self.show_collide_rects = False
        self.show_collide_masks = False
        self.show_objects = True

    def generate_asteroids(self, asteroids_number=20):
        asteroids = pg.sprite.Group()
        for _ in range(asteroids_number):
            x = random.randint(0, self.game.screen_res[0])
            y = random.randint(0, self.game.screen_res[1])
            asteroids.add(Asteroid(self, (x, y)))
        return asteroids

    def update(self):
        self.asteroids.update()
        # for asteroid in self.asteroids:
        #     asteroid.update()
        self.mouse.update()

    def draw(self):
        # self.asteroids.draw()
        for asteroid in self.asteroids:
            asteroid.draw()
        self.mouse.draw()


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
