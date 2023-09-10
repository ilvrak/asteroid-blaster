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
        self.battery = Battery()
        self.laser = Laser()

    def update(self):
        self.x += self.move_increment
        self.y = HEIGHT // 2 - math.sin(math.radians(self.x)) * HEIGHT // 8
        self.middle_y = self.y + self.width // 2
        self.nose = (self.x + self.length, self.middle_y)
        self.back = (self.x, self.middle_y)
        self.left_wing = (self.x, self.y)
        self.right_wing = (self.x, self.y + self.width)

    def update_systems(self):
        self.battery.update(self.back, self.nose)
        self.laser.update()

    def draw(self):
        points = [
            self.left_wing,
            self.right_wing,
            self.nose
        ]
        pg.draw.polygon(screen, 'white', points, 1)


class Laser:
    def __init__(self):
        self.width = 1
        self.color = 'red'
        self.energy_use = 10
        self.range = 100

    def update(self):
        pass

    def draw(self, ship):
        ship_nose = (ship.x + ship.length, ship.y + ship.width // 2)
        for asteroid in asteroids:
            asteroid_x, asteroid_y, asteroid_radius = asteroid
            distance = math.hypot(asteroid_x - ship.x, asteroid_y - ship.y)
            if distance < 100:
                if self.battery_fill == 1:
                    pg.draw.line(screen, self.color, ship_nose, (asteroid_x, asteroid_y), self.width)
                    asteroids.remove(asteroid)
                    self.last_shot_time = pg.time.get_ticks()
                    self.battery_fill = 0


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
        pg.draw.line(screen, laser.color, ship.back, (self.x + self.fill * self.length, ship.middle_y))


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


def draw_window():
        # Очистка экрана
        screen.fill('black')

        # Отрисовка астероидов
        for asteroid in asteroids:
            asteroid.draw()

        # # Обновление и отрисовка корабля
        ship.update()
        ship.draw()

        # Обновление экрана
        pg.display.flip()
        clock.tick(FPS)


def main():
    # Основной цикл программы
    running = True
    while running:
        # Обработка событий
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        draw_window()

    # Завершение программы
    pg.quit()

if __name__ == "__main__":
    main()
