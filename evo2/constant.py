import pygame as pg
import os

WIDTH, HEIGHT = 1024, 768
WIDTH_RANGE = (0, WIDTH*9//10)
HEIGHT_RANGE = (0, HEIGHT*9//10)
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Evolution simulator v0.2(Nightly)")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

IMAGE_SIZE = (75, 75)
BACKGROUND = pg.transform.scale(
    pg.image.load(os.path.join('Assets', 'grass_bg.jpg')), (WIDTH, HEIGHT)
)

RABBITS = []
WOLVES = []
GENOTYPE_STAT = {}

# Acromegaly = 말단 비대증
GENE_NAMES = ('Teeth', 'Speed', 'Color', 'Size', 'Time',
                  'Acromegaly', 'Metabolism', 'OxygenEffiency')
GENOTYPE = ('AA', 'Aa', 'aa')

ENV = {"Food type": ("Hard", "Soft"),
       "Predator": ("On", "Off"),
       "Ground": ("Grass", "Snow"),
       "Predator size": ("Big", "Small"),
       "Time" : ("Day", "Night"),
       "Temperature": ("Extreme", "Moderate"),
       "Food amount": ("Plenty", "Scarce"),
       "Altitude": ("High", "Low")
       }

CURRENT_ENV = {"Food type": 0,
       "Predator": -1,
       "Ground": -1,
       "Predator size": -1,
       "Time" : -1,
       "Temperature": -1,
       "Food amount": -1,
       "Altitude": -1
       }

ENV_DEATH_RATE = {
    "Food type Hard": ("Teeth", "A", 0.02),
    "Food type Soft": ("Teeth", "a", 0.5),
    "Predator On": ("Speed", "A", 0.5),
    "Predator Off": ("Speed", "a", 0.5),
    "Ground Grass": ("Color", "A", 0.5),
    "Ground Snow": ("Color", "a", 0.5),
    "Predator size Big": ("Size", "A", 0.5),
    "Predator size Small": ("Size", "a", 0.5),
    "Time Day": ("Time", "A", 0.5),
    "Time Night": ("Time", "a", 0.5),
    "Temperature Extreme": ("Acromegaly", "A", 0.5),
    "Temperature Moderate": ("Acromegaly", "a", 0.5),
    "Food amount Plenty": ("Metabolism", "A", 0.5),
    "Food amount Scarce": ("Metabolism", "a", 0.5),
    "Altitude High": ("OxygenEffiency", "A", 0.5),
    "Altitude Low": ("OxygenEffiency", "a", 0.5)
}