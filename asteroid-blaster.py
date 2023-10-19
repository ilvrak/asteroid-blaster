import math
import random

import pygame as pg

pg.init()
pg.display.set_caption("Asteroid Blaster")

RES = WIDTH, HEIGHT = 800, 600
MIDDLE_Y = HEIGHT // 2
FPS = 30
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()


class Ship:
    def __init__(self, width, length, x=0, y=MIDDLE_Y, frequency=1):
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

    def update(self):
        self.x += self.move_increment
        self.y = self.initial_y - math.sin(self.frequency * math.radians(self.x)) * HEIGHT // 8
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
        pg.draw.polygon(screen, 'white', self.points, self.armor)
        # pg.draw.rect(screen, 'magenta', self.rect, 1)

    def check_collision(self, ships, asteroids):
        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                # print(self.rect, asteroid.rect)
                ships.remove(self)
                asteroids.remove(asteroid)
                break


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
        pg.draw.line(screen, self.color, self.ship.nose, (target.x, target.y), self.width)
        asteroids.remove(target)
        self.ship.battery.charge -= self.ship.laser.energy_use


class Battery:
    def __init__(self, ship):
        self.ship = ship
        self.capacity = 100
        self.charge = self.capacity
        self.charge_speed = 1

    def update(self):
        if self.charge < self.capacity:
            self.charge += self.charge_speed
        pg.draw.line(screen, self.ship.laser.color, self.ship.back, (self.ship.x + self.charge * self.ship.length / self.capacity, self.ship.y))


class Asteroid:
    def __init__(self, x, y, radius):
        self.color = 'darkgray'
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def draw(self):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius, 1)
        # pg.draw.rect(screen, 'magenta', self.rect, 1)

    def hitted(self):
        self.radius
        pass

    @classmethod
    def generate(cls, num_asteroids, radius_range=(3, 10)):
        asteroids = []
        for _ in range(num_asteroids):
            asteroid_radius = random.randint(*radius_range)
            asteroid_x = random.randint(0, WIDTH)
            asteroid_y = random.randint(0, HEIGHT)
            asteroid = cls(asteroid_x, asteroid_y, asteroid_radius)
            asteroids.append(asteroid)
        return asteroids


# Генерация астероидов
asteroids = Asteroid.generate(200)

# Создание кораблей
ships = []
ships.append(Ship(20, 30))
ships.append(Ship(20, 30, -40, MIDDLE_Y - 30))
ships.append(Ship(20, 30, -50, MIDDLE_Y + 30))


def draw_screen():
    screen.fill('black')

    for asteroid in asteroids:
        asteroid.draw()

    for ship in ships:
        ship.update()
        ship.check_collision(ships, asteroids)
        ship.laser.scan(asteroids)
        ship.battery.update()

    pg.display.flip()


def main():
    running = True
    while running:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if len(ships) == 0 or ships[-1].x > WIDTH:
            running = False

        draw_screen()

    pg.quit()


if __name__ == "__main__":
    main()
