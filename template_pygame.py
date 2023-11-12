import sys

import pygame as pg


class Entity(pg.sprite.Sprite):
    def __init__(self, groups, image=pg.Surface((0, 0), pg.SRCALPHA), position=(0, 0)):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        ...


class Level:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class Game:
    def __init__(self, caption, screen_res, fps):
        pg.init()
        self.screen = pg.display.set_mode(screen_res)
        pg.display.set_caption(caption)
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.fps = fps
        self.running = True

        self.level = Level()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                ...

    def update(self):
        ...
        pg.display.flip()
        self.dt = self.clock.tick(self.fps)

    def draw(self):
        self.screen.fill('black')
        ...

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        self.close()

    def close(self):
        pg.quit()
        sys.exit()


def main():
    game = Game(caption='Some', screen_res=(640, 480), fps=60)
    game.run()


if __name__ == '__main__':
    main()
