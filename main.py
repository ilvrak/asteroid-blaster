import sys

import pygame as pg

from classes import Space
from settings import SCREEN_RES, SCREEN_WIDTH, FPS


# Game - (Space - (Asteroids - (Asteroid), Ships - (Ship - (Laser, Battery))), Menu)

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Asteroid Blaster")
        self.screen = pg.display.set_mode(SCREEN_RES)
        self.clock = pg.time.Clock()

        self.new_game()

    def new_game(self):
        self.running = True
        self.space = Space(self)

    def is_game_over(self):
        pass

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

    def update(self):
        self.space.update()

        pg.display.flip()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill('black')
        self.space.draw()

    def run(self):
        self.new_game()
        while self.running:
            self.check_events()
            self.update()
            self.draw()
            lose = len(self.space.ships) == 0
            win = self.space.ships[-1].x > SCREEN_WIDTH
            if lose or win:
                self.running = False
        self.close()

    def close(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
