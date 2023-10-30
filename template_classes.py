import pygame as pg
import sys


SCREEN_RES = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
FPS = 60


class Some:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class Game:
    def __init__(self, screen_res, fps):
        self.screen_res = screen_res
        pg.init()
        pg.display.set_caption('')
        self.screen = pg.display.set_mode(self.screen_res)
        self.clock = pg.time.Clock()
        self.fps = fps
        self.running = True

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                pass

    def update(self):
        self.clock.tick(self.fps)

    def draw(self):
        self.screen.fill('black')
        pg.display.flip()

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        self.close()

    def close(self):
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game(SCREEN_RES, FPS)
    game.run()
