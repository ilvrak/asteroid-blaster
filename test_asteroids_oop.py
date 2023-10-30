import pygame as pg
import random
import math
import sys


class Entity(pg.sprite.Sprite):
    def __init__(self, groups, image=pg.Surface((0,0), pg.SRCALPHA), position=(0,0)):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)


class Asteroid(pg.sprite.Sprite):
    def __init__(self, space, position=(0,0), size=4):
        super().__init__()
        self.space = space

        self.position = position
        self.size = size
        self.points = self.build_polygon(self.size)
        min_x, min_y = map(min, zip(*self.points))
        max_x, max_y = map(max, zip(*self.points))
        width = max_x - min_x + 3
        height = max_y - min_y + 3
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.rect.width = width
        self.rect.height = height
        pg.draw.polygon(self.image, 'darkgray', [(x - min_x + 1, y - min_y + 1) for x, y in self.points])
        self.mask = pg.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.image.fill(pg.SRCALPHA)
        pg.draw.polygon(self.image, 'darkgray', [(x - min_x + 1, y - min_y + 1) for x, y in self.points], 1)

        self.velocity = pg.math.Vector2()

    def build_polygon(self, mean) -> list[tuple[int]]:
        deviation = mean / 4
        radius = mean * 2
        vertices = random.randint(5, 15)
        angles = [i * 2 * math.pi / vertices for i in range(vertices)]

        polygon = []
        for angle in angles:
            rib_radius = min(random.gauss(mean, deviation), radius)
            x = self.position[0] + rib_radius * math.cos(angle)
            y = self.position[1] + rib_radius * math.sin(angle)
            polygon.append( (int(x), int(y)) )
        print(polygon)
        return polygon

    def split(self):
        new_size = self.size // 2
        new_position1 = (self.position[0] + random.randint(-self.size*2, self.size*2), self.position[1] + random.randint(-self.size*2, self.size*2))
        new_position2 = (self.position[0] + random.randint(-self.size*2, self.size*2), self.position[1] + random.randint(-self.size*2, self.size*2))
        shatter1 = Asteroid(self.space, new_position1, new_size)
        shatter2 = Asteroid(self.space, new_position2, new_size)
        return [shatter1, shatter2]

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


class Particle(pg.sprite.Sprite):
    def __init__(self, space, pos):
        super().__init__()
        self.space = space
        self.image = pg.Surface((1, 1))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel_x = random.randint(-5, 5)
        self.vel_y = random.randint(-5, 5)
        self.life = 10

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.life -= 1
        if self.life <= 0:
            self.kill()


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
            self.collide = 'Collided Rects!'
            self.color = 'blue'
            if collides := pg.sprite.spritecollide(self, self.space.asteroids, False, pg.sprite.collide_mask):
                self.collide = 'Collided Masks!'
                self.color = 'red'
                self.space.splash(collides[0].position)
                if collides[0].size < 4:
                    collides[0].kill()
                    return
                new_asteroids = collides[0].split()
                self.space.asteroids.remove(collides[0])
                self.space.asteroids.add(*new_asteroids)
        else:
            self.collide = 'Not Collided...'
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
        if self.space.print_collides:
            print(self.collide)


class Space:
    def __init__(self, game):
        self.game = game
        self.mouse = Mouse(self)
        self.asteroids = self.generate_asteroids(20)
        self.particles = pg.sprite.Group()
        self.sprites = pg.sprite.Group()
        self.entity = Entity([self.sprites])
        self.show_collide_rects = False
        self.show_collide_masks = False
        self.print_collides = False
        self.show_objects = True

    def generate_asteroids(self, asteroids_number=20) -> pg.sprite.Group:
        asteroids = pg.sprite.Group()
        for _ in range(asteroids_number):
            x = random.randint(0, self.game.screen_res[0])
            y = random.randint(0, self.game.screen_res[1])
            size = random.randint(30, 30)
            asteroids.add(Asteroid(self, (x, y), size))
        return asteroids

    def splash(self, epicenter):
        self.particles.add(*[Particle(self, epicenter) for _ in range(10)])

    def update(self):
        self.asteroids.update()
        self.particles.update()
        # for asteroid in self.asteroids:
        #     asteroid.update()
        self.mouse.update()

    def draw(self):
        self.game.screen.fill('black')
        # self.sprites.draw(self.game.screen)
        for asteroid in self.asteroids:
            asteroid.draw()
        self.particles.draw(self.game.screen)
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
        self.fps = fps

        self.space = Space(self)
        pg.mouse.set_visible(False)
        self.running = True

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
                if event.key == pg.K_t:
                    self.space.print_collides = not self.space.print_collides

    def update(self):
        self.space.update()
        pg.display.update()
        self.clock.tick(self.fps)

    def draw(self):
        self.space.draw()

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
