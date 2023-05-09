import pygame as pg
import os
from constant import *

class Button:

    def __init__(self, left: int, top: int, width: int, height: int, name: str) -> None:
        self.pos = (left, top, width, height)
        self.block = pg.Rect(*self.pos)
        self.pressed = False
        self.name = name
        self.text = FONT.render(self.name, True, BLACK)
    
    def toggle_if_clicked(self, x: int, y: int) -> bool:
        if self.block.collidepoint(x, y):
            self.pressed = not self.pressed
            if self.pressed:
                print('Current environment is:', self.name)
            return True

    def get_pressed(self) -> bool:
        return self.pressed

    def get_background(self) -> pg.Surface:
        if self.name.startswith('Arctic'):
            return pg.image.load(os.path.join('Assets', 'snow_bg.jpg'))
        elif self.name.startswith('Amazon'):
            return pg.image.load(os.path.join('Assets', 'grass_bg.jpg'))
        elif self.name.startswith('Desert'):
            return pg.image.load(os.path.join('Assets', 'desert_bg.jpg'))
    
    def get_rect(self) -> pg.Rect:
        return self.block

    def get_name(self) -> str:
        return self.name

    def get_text(self) -> pg.Surface:
        return self.text

    def get_pos(self) -> tuple:
        return self.pos
