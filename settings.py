import pygame as py

class Settings:
    def __init__(self):
        self.width = 720
        self.length = 480

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 255, 0)
        self.GREEN = (0, 0, 255)

        self.screen = py.display.set_mode((self.width, self.length))