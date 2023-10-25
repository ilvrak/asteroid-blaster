import sys

import pygame as pg

from classes import Ship, Asteroid
from settings import SCREEN_RES, MIDDLE_Y, SCREEN_WIDTH


# Game - (Space - (Asteroids - (Asteroid), Ships - (Ship - (Laser, Battery))), Menu)

class Game:
    def __init__(self):

        pg.init()
        pg.display.set_caption("Asteroid Blaster")

        self.screen = pg.display.set_mode(SCREEN_RES)
        self.clock = pg.time.Clock()

        self.new_game()

    def new_game(self):
        # Генерация астероидов
        self.asteroids = Asteroid.generate(200)

        # Создание кораблей
        self.ships = []
        self.ships.append(Ship(self, 20, 30, -10))
        self.ships.append(Ship(self, 20, 30, -50, MIDDLE_Y - 30))
        self.ships.append(Ship(self, 20, 30, -60, MIDDLE_Y + 30))

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

    def is_game_over(self):
        pass

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        self.new_game()
        running = True
        while running:
            self.check_events()
            self.update()
            self.draw()
            lose = len(self.ships) == 0
            win = self.ships[-1].x > SCREEN_WIDTH
            if lose or win:
                running = False


if __name__ == "__main__":
    game = Game()
    game.run()
