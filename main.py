
import sys

import pygame as pg
import pygame.freetype as ft

from game_objects import *


class Game:
    def __init__(self):

        self.RES = self.WIDTH, self.HEIGHT = 800, 600
        self.FONT_SIZE = 40
        self.MIDDLE_Y = self.HEIGHT // 2
        self.FPS = 30

        pg.init()
        pg.display.set_caption("Asteroid Blaster")

        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.font = ft.SysFont('Verdana', self.FONT_SIZE)

        self.new_game()

    def new_game(self):
        # Генерация астероидов
        self.asteroids = Asteroid.generate(200)

        # Создание кораблей
        self.ships = []
        self.ships.append(Ship(20, 30, -10))
        self.ships.append(Ship(20, 30, -50, self.MIDDLE_Y - 30))
        self.ships.append(Ship(20, 30, -60, self.MIDDLE_Y + 30))

    def update(self):
        for ship in self.ships:
            ship.update()
            ship.check_collision(self.ships, self.asteroids)
            ship.laser.scan(self.asteroids)
            ship.battery.update()

        pg.display.flip()
        self.clock.tick(self.FPS)

    def draw(self):
        self.screen.fill('black')

        for asteroid in self.asteroids:
            asteroid.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        running = True
        while running:
            self.check_events()
            self.update()
            self.draw()
            lose = len(self.ships) == 0
            win = self.ships[-1].x > self.WIDTH
            if lose or win:
                running = False


if __name__ == "__main__":
    game = Game()
    game.run()
