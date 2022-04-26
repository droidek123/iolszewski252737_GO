""" Main module"""

import pygame
from gui.view import View


def main():
    """Main method"""
    view = View()
    view.init_pygame()
    view.draw()

    while True:
        view.update()
        pygame.time.wait(100)


if __name__ == "__main__":
    main()
