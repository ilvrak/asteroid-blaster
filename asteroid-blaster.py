import pygame as pg
import math
import random

pg.init()
pg.display.set_caption("Космический корабль")

RES = WIDTH, HEIGHT = 800, 600
FPS = 30
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()


# Параметры космического корабля
ship_width = 20
ship_length = 30

# Начальные координаты корабля
ship_x = 0
ship_y = HEIGHT // 2

# Количество пикселей, на которое корабль сдвигается по X за одну итерацию
move_increment = 1

# Параметры лазера
laser_width = 1
laser_color = 'red'
laser_cooldown = 300
last_shot_time = 0

# Генерация астероидов
asteroid_radius_range = (5, 10)
asteroid_number = 100
asteroids = []
for _ in range(asteroid_number):
    asteroid_radius = random.randint(*asteroid_radius_range)
    asteroid_x = random.randint(0, WIDTH)
    asteroid_y = random.randint(0, HEIGHT)
    asteroids.append((asteroid_x, asteroid_y, asteroid_radius))



# Основной цикл программы
running = True
while running:
    # Обработка событий
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Очистка экрана
    screen.fill('black')


    # Рисование и позиционирование космического корабля
    ship_nose = (ship_x + ship_length, ship_y + ship_width // 2)
    ship_points = [
        (ship_x, ship_y),
        (ship_x, ship_y + ship_width),
        ship_nose
    ]

    pg.draw.polygon(screen, 'white', ship_points, 1)

    # Расчет новых координат корабля
    ship_x += move_increment
    ship_y = HEIGHT // 2 - math.sin(math.radians(ship_x)) * HEIGHT // 8

    # Если корабль заходит за правый край экрана, возвращаем его в начало
    if ship_x > WIDTH:
        running = False


    # Рисование астероидов
    for asteroid in asteroids:
        asteroid_x, asteroid_y, asteroid_radius = asteroid
        pg.draw.circle(screen, 'darkgray', (asteroid_x, asteroid_y), asteroid_radius, 1)

    # Рисование лазера и проверка столкновения с астероидами
    current_time = pg.time.get_ticks()
    for asteroid in asteroids:
        asteroid_x, asteroid_y, asteroid_radius = asteroid

        # Проверка, расстояние от корабля до астероида
        distance = math.hypot(asteroid_x - ship_x, asteroid_y - ship_y)
        if distance < 100:
            if current_time - last_shot_time > laser_cooldown:
                # Рисование лазера
                pg.draw.line(screen, laser_color, ship_nose, (asteroid_x, asteroid_y), laser_width)

                # Удаление астероида
                asteroids.remove(asteroid)

                # Обновление времени последнего выстрела
                last_shot_time = current_time

    # Обновление экрана
    pg.display.flip()
    clock.tick(FPS)

# Завершение программы
pg.quit()
