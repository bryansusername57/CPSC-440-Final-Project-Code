import pygame as py
from settings import Settings

class Car:
    def __init__(self, color, pos1, pos2):
        super().__init__()
        self.settings = Settings()
        self.color = color
        self.image = py.Surface((32,32))
        self.image.fill(color)
        self.rect = py.Rect((pos1, pos2), (32, 32))

    def update(self):
        self.screen.blit(self.image, self.rect)