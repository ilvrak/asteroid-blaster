from settings import MIDDLE_Y, SCREEN_WIDTH, SCREEN_HEIGHT

import math
import random
import pygame as pg

vec2 = pg.math.Vector2


class Ship:
    def __init__(self, space, width, length, x=0, y=MIDDLE_Y, frequency=1):
        self.space = space
        self.width = width
        self.length = length
        self.x = x
        self.y = y
        self.frequency = frequency
        self.initial_y = y
        self.move_increment = 1
        self.armor = 1
        self.battery = Battery(self)
        self.laser = Laser(self)
        self.rect = pg.Rect(self.x, self.y - self.width // 2, self.length, self.width)

    def check_collision(self, ships, asteroids):
        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                # print(self.rect, asteroid.rect)
                ships.remove(self)
                asteroids.remove(asteroid)
                break

    def update(self):
        self.x += self.move_increment
        self.y = self.initial_y - math.sin(self.frequency * math.radians(self.x)) * SCREEN_HEIGHT // 8
        self.back = (self.x, self.y)
        self.nose = (self.x + self.length, self.y)
        self.left_wing = (self.x, self.y - self.width // 2)
        self.right_wing = (self.x, self.y + self.width // 2)
        self.rect = pg.Rect(self.x, self.y - self.width // 2, self.length, self.width)
        self.points = [
            self.left_wing,
            self.right_wing,
            self.nose
        ]
        pg.draw.polygon(self.space.game.screen, 'white', self.points, self.armor)
        # pg.draw.rect(screen, 'magenta', self.rect, 1)

    def draw(self):
        pass


class Laser:
    def __init__(self, ship):
        self.ship = ship
        self.width = 1
        self.color = 'red'
        self.energy_use = 20
        self.range = 100

    def scan(self, asteroids):
        nearest_asteroid = None
        nearest_distance = float('inf')
        for asteroid in asteroids:
            distance = math.hypot(asteroid.x - self.ship.nose[0], asteroid.y - self.ship.nose[1])
            if distance < self.range:
                if distance < nearest_distance:
                    nearest_asteroid = asteroid
                    nearest_distance = distance
        if nearest_asteroid is not None and self.ship.battery.charge >= self.ship.laser.energy_use:
            self.shoot(nearest_asteroid)

    def shoot(self, target):
        pg.draw.line(self.ship.space.game.screen, self.color, self.ship.nose, (target.x, target.y), self.width)
        self.ship.space.asteroids.remove(target)
        self.ship.battery.charge -= self.ship.laser.energy_use

    def update(self):
        pass

    def draw(self):
        pass


class Battery:
    def __init__(self, ship):
        self.ship = ship
        self.capacity = 100
        self.charge = self.capacity
        self.charge_speed = 1

    def update(self):
        if self.charge < self.capacity:
            self.charge += self.charge_speed
        pg.draw.line(self.ship.space.game.screen, self.ship.laser.color, self.ship.back,
                     (self.ship.x + self.charge * self.ship.length / self.capacity, self.ship.y))

    def draw(self):
        pass


class Asteroid:
    def __init__(self, space, x, y, radius):
        self.space = space
        self.color = 'darkgray'
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        pass

    def draw(self):
        pg.draw.circle(self.space.game.screen, self.color, (self.x, self.y), self.radius, 1)
        # pg.draw.rect(self.space.game.screen, 'magenta', self.rect, 1)


class Space:
    def __init__(self, game):
        self.game = game
        self.asteroids = self.generate_asteroids()
        self.ships = self.create_ships()

    def generate_asteroids(self, num_asteroids=200, radius_range=(3, 10)):
        asteroids = []
        for _ in range(num_asteroids):
            asteroid_radius = random.randint(*radius_range)
            asteroid_x = random.randint(0, SCREEN_WIDTH)
            asteroid_y = random.randint(0, SCREEN_HEIGHT)
            asteroid = Asteroid(self, asteroid_x, asteroid_y, asteroid_radius)
            asteroids.append(asteroid)
        return asteroids

    def create_ships(self):
        ships = []
        ships.append(Ship(self, 20, 30, -10))
        ships.append(Ship(self, 20, 30, -50, MIDDLE_Y - 30))
        ships.append(Ship(self, 20, 30, -60, MIDDLE_Y + 30))
        return ships

    def update(self):
        for ship in self.ships:
            ship.update()
            ship.check_collision(self.ships, self.asteroids)
            ship.laser.scan(self.asteroids)
            ship.battery.update()

    def draw(self):
        for ship in self.ships:
            ship.draw()
        for asteroid in self.asteroids:
            asteroid.draw()

class Menu:
    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self):
        pass
