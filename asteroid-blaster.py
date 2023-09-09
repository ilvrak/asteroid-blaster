import pygame
import math

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
    points = [
        (ship_x, ship_y),
        (ship_x, ship_y + ship_width),
        (ship_x + ship_length, ship_y + ship_width // 2)
    ]

    pygame.draw.polygon(screen, 'white', points, 1)

    # Расчет новых координат корабля
    ship_x += move_increment
    ship_y = screen_height // 2 - math.sin(math.radians(ship_x)) * screen_height // 8

    # Если корабль заходит за правый край экрана, возвращаем его в начало
    if ship_x > screen_width:
        ship_x = 0

    # Обновление экрана
    pygame.display.flip()    

# Завершение программы
pygame.quit()
