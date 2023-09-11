import pygame as pg
import math
import random

pg.init()
pg.display.set_caption("Asteroid Blaster")

RES = WIDTH, HEIGHT = 800, 600
FPS = 30
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()


class Ship:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        # Начальные координаты корабля
        self.x = 0
        self.y = HEIGHT // 2
        self.move_increment = 1
        self.armor = 1
        self.battery = Battery()
        self.laser = Laser()

    def update(self):
        self.x += self.move_increment
        self.y = HEIGHT // 2 - math.sin(math.radians(self.x)) * HEIGHT // 8
        self.back = (self.x, self.y)
        self.nose = (self.x + self.length, self.y)
        self.left_wing = (self.x, self.y - self.width // 2)
        self.right_wing = (self.x, self.y + self.width // 2)
        self.points = [
            self.left_wing,
            self.right_wing,
            self.nose
        ]
        pg.draw.polygon(screen, 'white', self.points, self.armor)

    def update_systems(self):
        self.battery.update(self.back, self.nose)

    def shoot_laser(self):
        self.laser.shoot()

    def collide(self):
        self.armor -= 1


class Laser:
    def __init__(self):
        self.width = 1
        self.color = 'red'
        self.energy_use = 10
        self.range = 100

    def scan(self, asteroids):
        for asteroid in asteroids:
            distance = math.hypot(asteroid.x - ship.nose[0], asteroid.y - ship.nose[1])
            if distance < self.range:
                self.shoot(asteroid)

    def shoot(self, target):
        pg.draw.line(screen, self.color, ship.nose, (target.x, target.y), self.width)
        asteroids.remove(target)


class Battery:
    def __init__(self):
        self.capacity = 100
        self.fill = 1
        self.charge_speed = 1

    def update(self):
        current_time = pg.time.get_ticks()
        if (current_time - self.last_shot_time) >= self.cooldown:
            self.battery_fill = 1
        else:
            self.battery_fill = (current_time - self.last_shot_time) / self.cooldown

    def draw(self):
        pg.draw.line(screen, ship.laser.color, ship.back, (self.x + self.fill * ship.length, ship.y))


class Asteroid:
    # у астеройда не будет толщины брони
    # крепкость астеройда не будет определяться их радиусом
    # вместо этого выстрел по астеройду будет делить его на две части, но каждая не меньше минимального радиуса, рандомного радиуса от деления
    # осколки генерируются в радиусе 20 от исходного
    # столкновение генерирует событие распада астеройда, такое же как при попадании лазера
    # при столкновении корабль теряет единицу брони
    def __init__(self, x, y, radius):
        self.color = 'darkgray'
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius, 1)

    def hitted(self):
        pass

    @classmethod
    def generate(cls, num_asteroids, radius_range=(3, 10)):
        radius_min = radius_range[0]
        radius_max = radius_range[-1]
        asteroids = []
        for _ in range(num_asteroids):
            asteroid_radius = random.randint(*radius_range)
            asteroid_x = random.randint(0, WIDTH)
            asteroid_y = random.randint(0, HEIGHT)
            asteroid = cls(asteroid_x, asteroid_y, asteroid_radius)
            asteroids.append(asteroid)
        return asteroids


# Генерация астероидов
asteroids = Asteroid.generate(100)

# Создание корабля
ship = Ship(20, 30)


def draw_screen():
    screen.fill('black')

    for asteroid in asteroids:
        asteroid.draw()

    ship.update()
    ship.laser.scan(asteroids)

    pg.display.flip()


def main():
    running = True
    while running:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if ship.x > WIDTH:
            running = False

        draw_screen()

    pg.quit()

if __name__ == "__main__":
    main()
