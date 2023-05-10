import pygame as pg
from os import path

pg.init()

WIDTH, HEIGHT = 1024, 768
WIDTH_RANGE = (0, WIDTH*9//10)
HEIGHT_RANGE = (HEIGHT*2//10, HEIGHT*9//10)
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Evolution simulator v0.5")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RECT_NOCLICK_COLOR = WHITE
RECT_CLICK_COLOR = (200, 200, 200)
PADDING = 5

IMAGE_SIZE = (75, 75)
BACKGROUND = pg.transform.scale(
    pg.image.load(path.join('Assets', 'grass_bg.jpg')), (WIDTH, HEIGHT)
)
BUTTON_BACKGROUND = pg.Rect(0, 0, WIDTH, HEIGHT//10+PADDING)

FONT = pg.font.SysFont(pg.font.get_default_font(), 30, True)

RABBITS = []
#WOLVES = []
GENOTYPE_STAT = {}
AGE_STAT = {}
CHILDS_STAT = {}
BUTTONS = []

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

HIGH_DEATH_RATE = 5
MID_DEATH_RATE = 2
LOW_DEATH_RATE = 1

ENV_DEATH_RATE = {
    # WHITE, FAST, LONG
    "Arctic A":  {'Color': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Speed': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Fur': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE)},

    # WHITE, SLOW, SHORT
    "Arctic B":  {'Color': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Speed': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Fur': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE)},

    # CAMOUFLAGE, FAST, LONG
    "Amazon A":  {'Color': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Speed': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Fur': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE)},

    # CAMOUFLAGE, SLOW, SHORT
    "Amazon B":  {'Color': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Speed': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Fur': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE)},

    # CAMOUFLAGE, FAST, SHORT
    "Desert A":  {'Color': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Speed': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Fur': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE)},

    # CAMOUFLAGE, SLOW, SHORT
    "Desert B":  {'Color': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE),
                 'Speed': (HIGH_DEATH_RATE, MID_DEATH_RATE, LOW_DEATH_RATE),
                 'Fur': (LOW_DEATH_RATE, MID_DEATH_RATE, HIGH_DEATH_RATE)},
}