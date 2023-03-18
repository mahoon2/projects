import pygame as pg
import os
import random

WIDTH, HEIGHT = 1024, 600
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Evolution simulator v0.1")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

IMAGE_SIZE = (100, 100)
RABBIT = pg.transform.scale(
    pg.image.load(os.path.join('evo', 'Assets', 'rabbit.png')), IMAGE_SIZE
)
WOLF = pg.transform.scale(
    pg.image.load(os.path.join('evo', 'Assets', 'wolf.png')), IMAGE_SIZE
)
BACKGROUND = pg.transform.scale(
    pg.image.load(os.path.join('evo', 'Assets', 'grass.jpg')), (WIDTH, HEIGHT)
)

class Rabbit:
    def __init__(self, image_name, x, y):
        # surface object
        self.sf = pg.transform.scale(
    pg.image.load(os.path.join('evo', 'Assets', image_name)), IMAGE_SIZE)
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x, self.y)
    
    def get_blit(self):
        return (self.sf, self.get_pos())
    
    def is_dead(self):
        pass

    def is_reproducing(self):
        pass

class Gene:
    def __init__(self, name):
        pass

def draw_window():
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(RABBIT, (0, 0))
    WINDOW.blit(WOLF, (100, 100))
    pg.display.update()

def main():
    running = True
    fps = 30
    fps_limit = 600
    clock = pg.time.Clock()

    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        draw_window()
        
    
    pg.quit()

if __name__ == '__main__':
    main()