"""
Arcade template
"""

import arcade


# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Some"


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        # Call the parent __init__
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        ...

    def on_update(self, dt):
        """ Move everything """
        ...

    def on_draw(self):
        """ Render the screen. """
        # Clear teh screen
        self.clear()
        ...


def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
