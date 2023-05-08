import pygame as pg
import os

WIDTH, HEIGHT = 1024, 768
WIDTH_RANGE = (0, WIDTH*9//10)
HEIGHT_RANGE = (0, HEIGHT*9//10)
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Evolution simulator v0.3(Nightly)")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RECT_NOCLICK_COLOR = (200, 200, 200)
RECT_CLICK_COLOR = (100, 100, 100)

IMAGE_SIZE = (75, 75)
BACKGROUND = pg.transform.scale(
    pg.image.load(os.path.join('Assets', 'grass_bg.jpg')), (WIDTH, HEIGHT)
)

RABBITS = []
#WOLVES = []
GENOTYPE_STAT = {}

GENE_NAMES = ('Color', 'Speed', 'Fur')
GENOTYPE = ('AA', 'Aa', 'aa')
GENOTYPE_NAMES = {
    'Color': ('Camouflage', 'White'),
    'Speed': ('Fast', 'Slow'),
    'Fur': ('Short', 'Long')
}

ENV_NAMES = (
    "Arctic A",
    "Arctic B",
    "Amazon A",
    "Amazon B",
    "Desert A",
    "Desert B"
)

CURRENT_ENV = "Arctic A"
HIGH_DEATH_RATE = 0.04
MID_DEATH_RATE = 0.02
LOW_DEATH_RATE = 0.01

ENV_DEATH_RATE = {
    "Arctic A":  {'Color': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Speed': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Fur': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE)},

    "Arctic B":  {'Color': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Speed': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Fur': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE)},

    "Amazon A":  {'Color': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Speed': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Fur': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE)},

    "Amazon B":  {'Color': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Speed': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Fur': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE)},

    "Desert A":  {'Color': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Speed': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Fur': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE)},

    "Desert B":  {'Color': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Speed': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Fur': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE)},
}