import pygame
import math
import random

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Космический корабль")


# Параметры космического корабля
ship_width = 20
ship_length = 30

# Начальные координаты корабля
ship_x = 0
ship_y = screen_height // 2

# Количество градусов, на которые корабль поворачивается за одну итерацию
rotation_speed = 1

# Количество пикселей, на которое корабль сдвигается по X за одну итерацию
move_increment = 0.01

# Параметры лазера
laser_width = 1
laser_color = 'red'

# Генерация астероидов
asteroid_radius_range = (5, 10)
asteroids = []
for _ in range(100):
    asteroid_radius = random.randint(*asteroid_radius_range)
    asteroid_x = random.randint(0, screen_width)
    asteroid_y = random.randint(0, screen_height)
    asteroids.append((asteroid_x, asteroid_y, asteroid_radius))



# Основной цикл программы
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill('black')


    # Рисование и позиционирование космического корабля
    ship_nose = (ship_x + ship_length, ship_y + ship_width // 2)
    points = [
        (ship_x, ship_y),
        (ship_x, ship_y + ship_width),
        ship_nose
    ]

    pygame.draw.polygon(screen, 'white', points, 1)

    # Расчет новых координат корабля
    ship_x += move_increment
    ship_y = screen_height // 2 - math.sin(math.radians(ship_x)) * screen_height // 8

    # Если корабль заходит за правый край экрана, возвращаем его в начало
    if ship_x > screen_width:
        running = False


    # Рисование астероидов
    for asteroid in asteroids:
        asteroid_x, asteroid_y, asteroid_radius = asteroid
        pygame.draw.circle(screen, 'darkgray', (asteroid_x, asteroid_y), asteroid_radius, 1)


    # Рисование лазера и проверка столкновения с астероидами
    for asteroid in asteroids:
        asteroid_x, asteroid_y, asteroid_radius = asteroid

        # Проверка, расстояние от корабля до астероида
        distance = math.hypot(asteroid_x - ship_x, asteroid_y - ship_y)
        if distance < 100:
            # Рисование лазера
            pygame.draw.line(screen, laser_color, ship_nose, (asteroid_x, asteroid_y), laser_width)
            asteroids.remove(asteroid)


    # Обновление экрана
    pygame.display.flip()

# Завершение программы
pygame.quit()
