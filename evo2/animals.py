import pygame as pg
import random
import math
import os
from constant import *

class Sprite:

    def __init__(self, x: int, y: int):
        self.age = 0
        self.x = x
        self.y = y
        self.theta = math.radians(random.randint(0, 359))
    
    def get_pos(self):
        return (self.x, self.y)
    
    def get_blit(self):
        return (self.sf, (self.x, self.y))
    
    def time_passed(self):
        # 0 for nothing
        # -1 for death
        # 1 for reproducing

        self.age += 1
        self.move()
        if self.is_dead(): return -1
        elif self.is_reproducing(): return 1
        else: return 0
    
    def is_dead(self):
        return False
    
    def is_reproducing(self):
        return False

class Rabbit(Sprite):

    REPRODUCE_THRESOLD = 10
    # Argument for pick_probability
    REPRODUCE_RATE = [1, 7]
    DEATH_THRESOLD = 70
    SPEED = 50
    MOVE_MOD = 5

    def __init__(self, gene_dict: dict, x: int, y: int):
        super().__init__(x, y)
        self.gene = gene_dict
        self.speed = Rabbit.SPEED
        self.sf = pg.transform.scale(
            pg.image.load(self.get_image_path()), IMAGE_SIZE
        )
    
    def get_genes(self):
        return self.gene
    
    def get_image_path(self):
        # 특정 Gene의 표현형에 따라 파일을 다르게 할 수도 있음
        return os.path.join('Assets', 'pixel_rabbit.png')

    def move(self):
        if self.age % self.MOVE_MOD == 0:
            self.theta = math.radians(random.randint(0, 360))
        self.x += int(self.speed * math.cos(self.theta))
        self.y += int(self.speed * math.sin(self.theta))

        if self.x < 0: self.x = 10 - self.x
        elif self.x >= WIDTH: self.x = 2*WIDTH - self.x - 10

        if self.y < 0: self.y = 10 - self.y
        elif self.y >= HEIGHT: self.y = 2*HEIGHT - self.y - 10
    
    def is_dead(self):
        if self.age >= Rabbit.DEATH_THRESOLD:
            return True
        for env, val in iter(CURRENT_ENV.items()):
            pass

            '''if val == -1: continue
            else:
                env_join = env + ' ' + ENV[env][val]
                gene_name, genotype, death_rate = ENV_DEATH_RATE[env_join]
                if genotype in self.gene[gene_name]:
                    prob_list = [death_rate*100, 100-(death_rate*100)]
                    return [True, False][pick_by_probability(prob_list)]'''

        return False

    def is_reproducing(self):
        if self.age < Rabbit.REPRODUCE_THRESOLD:
            return False
        else:
            return random.choices([True, False], weights=Rabbit.REPRODUCE_RATE)[0]
    
    def parse_gene(self):
        # 현재 켜져 있지 않은 환경(-1)은 무시한다.
        # ex) 유전자형 상으로 사이즈나 속도가 달라도 해당 환경이 꺼져 있으면 고려하지 않는다. 
        for env, val in iter(CURRENT_ENV.items()):
            if val == -1: continue
            key = env + ' ' + val

# END of class Rabbit

class Wolf(Sprite):

    REPRODUCE_THRESOLD = 10
    DEATH_THRESOLD = 70
    SPEED = 70

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.speed = Wolf.SPEED
        self.eaten_num = 0
        self.sf = pg.transform.scale(
            pg.image.load(self.get_image_path()), IMAGE_SIZE
        )
    
    def get_image_path(self):
        return os.path.join('Assets', 'pixel_wolf.png')

    def move(self):
        self.x += int(self.speed * math.cos(self.theta))
        self.y += int(self.speed * math.sin(self.theta))

        if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT:
            self.x = random.randint(*WIDTH_RANGE)
            self.y = random.randint(*HEIGHT_RANGE)
            self.theta = math.radians(random.randint(0, 359))

    def is_dead(self):
        if self.age >= Wolf.DEATH_THRESOLD:
            return True
        return False
    
    def is_reproducing(self):
        if self.eaten_num >= Wolf.REPRODUCE_THRESOLD:
            self.eaten_num = 0
            return True
        return False

    def eat(self):
        self.eaten_num += 1
      

# END of class Wolf