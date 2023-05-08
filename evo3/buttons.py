import pygame as pg
from constant import *

class Button:

    def __init__(self, left: int, top: int, width: int, height: int, name: str) -> None:
        self.pos = (left, top, width, height)
        self.block = pg.draw.rect(WINDOW, RECT_NOCLICK_COLOR, self.pos)
        self.pressed = False
        self.name = name
    
    def toggle_if_clicked(self, x: int, y: int) -> None:
        if self.block.collidepoint(x, y):
            pressed = not pressed
            if pressed:
                self.block = pg.draw.rect(WINDOW, RECT_CLICK_COLOR, self.pos)
                CURRENT_ENV = self.name
            else:
                self.block = pg.draw.rect(WINDOW, RECT_NOCLICK_COLOR, self.pos)