import pygame as pg
import matplotlib.pyplot as plt
import os
import random
from constant import *

class Rabbit:
    REPRODUCE_THRESOLD = 3
    # Argument for pick_probability
    REPRODUCE_RATE = [1, 2]
    DEATH_THRESOLD = 10

    def __init__(self, gene_dict: dict):
        # surface object
        self.age = 0
        self.gene = gene_dict
        self.sf = pg.transform.scale(
    pg.image.load(self.get_image_path()), IMAGE_SIZE)
    
    def get_blit(self):
        return (self.sf, (random.randint(*WIDTH_RANGE), random.randint(*HEIGHT_RANGE)))
    
    def get_genes(self):
        return self.gene
    
    def get_image_path(self):
        # 특정 Gene의 표현형에 따라 파일을 다르게 할 수도 있음
        return os.path.join('Assets', 'pixel_rabbit.png')

    def time_passed(self):
        # 0 for nothing
        # -1 for death
        # 1 for reproducing

        self.age += 1
        if self.is_dead(): return -1
        elif self.is_reproducing(): return 1
        else: return 0
    
    def is_dead(self):
        if self.age >= Rabbit.DEATH_THRESOLD:
            return True
        for env, val in iter(CURRENT_ENV.items()):
            if val == -1: continue
            else:
                env_join = env + ' ' + ENV[env][val]
                gene_name, genotype, death_rate = ENV_DEATH_RATE[env_join]
                if genotype in self.gene[gene_name]:
                    prob_list = [death_rate*100, 100-(death_rate*100)]
                    return [True, False][pick_by_probability(prob_list)]

        return False

    def is_reproducing(self):
        if self.age < Rabbit.REPRODUCE_THRESOLD:
            return False
        else:
            return [True, False][pick_by_probability(Rabbit.REPRODUCE_RATE)]

def gene_reproduce(father_gene: dict, mother_gene: dict) -> dict:
    ret = dict()

    for name in GENE_NAMES:
        temp1 = father_gene[name]
        temp2 = mother_gene[name]
        ret[name] = temp1[random.randint(0, 1)] + temp2[random.randint(0, 1)]
        if ret[name] == 'aA':
            ret[name] = 'Aa'
    
    return ret

def pick_by_probability(prob: list) -> int:
    # Input : list of positive integers
    # Output : Integer in range(0, len(list))

    ret = random.randint(1, sum(prob))
    s = 0
    for i in range(len(prob)):
        s += prob[i]
        if s >= ret:
            return i

def draw_window():
    WINDOW.blit(BACKGROUND, (0, 0))
    
    # 화면에 보이는 토끼 * 100 = 실제 토끼
    for i in range(0, len(RABBITS), 100):
        rabbit = RABBITS[i]
        WINDOW.blit(*rabbit.get_blit())
    
    pg.display.update()

def rabbit_time_passed():
    reproducing_rabbits = []
    dead_rabbits = []

    for i, rabbit in enumerate(RABBITS):
        ret = rabbit.time_passed()
        if ret == -1:
            dead_rabbits.append(i)
        elif ret == 1:
            reproducing_rabbits.append(rabbit)
    
    cnt = 0
    for i in sorted(dead_rabbits):
        deleted_genes_dict = RABBITS[i-cnt].get_genes()
        for gene, genotype in iter(deleted_genes_dict.items()):
            GENOTYPE_STAT[gene][genotype] -= 1
        del RABBITS[i-cnt]
        cnt += 1
    
    while len(reproducing_rabbits) >= 2:
        i = random.randint(0, len(reproducing_rabbits)-1)
        j = random.randint(0, len(reproducing_rabbits)-1)
        if i == j: continue
        if i > j:
            i, j = j, i
        new_gene_dict = gene_reproduce(reproducing_rabbits[i].get_genes(),
                                       reproducing_rabbits[j].get_genes())
        
        for gene, genotype in iter(new_gene_dict.items()):
            GENOTYPE_STAT[gene][genotype] += 1

        RABBITS.append(Rabbit(new_gene_dict))
        del reproducing_rabbits[i]
        del reproducing_rabbits[j-1]

x = dict.fromkeys(GENE_NAMES, list())
y1 = dict.fromkeys(GENE_NAMES, list())
y2 = dict.fromkeys(GENE_NAMES, list())
time = 0

def print_genostat(gene_name):
    s = 2*sum(GENOTYPE_STAT[gene_name].values())
    ret = (round((2*GENOTYPE_STAT[gene_name]['AA'] + GENOTYPE_STAT[gene_name]['Aa'])/s, 2),
           round((GENOTYPE_STAT[gene_name]['Aa'] + 2*GENOTYPE_STAT[gene_name]['aa'])/s, 2))

    global time
    x[gene_name].append(time)
    y1[gene_name].append(ret[0])
    y2[gene_name].append(ret[1])
    time += 1

    plt.cla()
    plt.plot(x[gene_name], y1[gene_name], label='A')
    plt.plot(x[gene_name], y2[gene_name], label='a')
    plt.suptitle('Allele frequency')
    plt.xlabel('time')
    plt.ylabel('frequency')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.pause(0.1)

def initialize_rabbit(num):
    # AA 1/4, Aa 1/2, aa 1/4 의 비율로 토끼를 만든다
    # GENOTYPE_STAT을 초기화한다

    gene_cnt = dict()
    for name in GENE_NAMES:
        gene_cnt[name] = {'AA':num//4, 'Aa':num//2, 'aa':num//4}
        GENOTYPE_STAT[name] = {'AA':0, 'Aa':0, 'aa':0}

    for _ in range(num):
        new_gene_dict = dict.fromkeys(GENE_NAMES)

        for name in GENE_NAMES:
            picked_genotype = GENOTYPE[pick_by_probability([gene_cnt[name][key]
                                                                for key in GENOTYPE])]
            new_gene_dict[name] = picked_genotype
            gene_cnt[name][picked_genotype] -= 1
            GENOTYPE_STAT[name][picked_genotype] += 1

        RABBITS.append(Rabbit(new_gene_dict))

def main():
    running = True
    paused = True
    fps = 10
    #fps_limit = 600
    clock = pg.time.Clock()

    draw_window()
    initial_rabbit = 500
    max_rabbits = 10000
    initialize_rabbit(initial_rabbit)

    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_p]:
                    paused = False
        
        if len(RABBITS) >= max_rabbits or len(RABBITS) <= 1:
            running = False
        
        if not paused:
            print('Current num of rabbits: ', len(RABBITS))
            rabbit_time_passed()
            draw_window()

            CURRENT_ENV["Food type"] = 0
            print_genostat("Teeth")
            '''for gene_name in GENE_NAMES:
                print_genostat(gene_name)'''
    
    plt.show()
    pg.quit()

if __name__ == '__main__':
    main()