import pygame as pg
import matplotlib.pyplot as plt
import os
import random

WIDTH, HEIGHT = 1024, 768
WIDTH_RANGE = (0, WIDTH*9//10)
HEIGHT_RANGE = (HEIGHT*2//5, HEIGHT*9//10)
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Evolution simulator v0.1")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

IMAGE_SIZE = (100, 100)
'''RABBIT = pg.transform.scale(
    pg.image.load(os.path.join('evo', 'Assets', 'rabbit (1).png')), IMAGE_SIZE
)
WOLF = pg.transform.scale(
    pg.image.load(os.path.join('evo', 'Assets', 'wolf.png')), IMAGE_SIZE
)'''
BACKGROUND = pg.transform.scale(
    pg.image.load(os.path.join('evo', 'Assets', 'grass_bg.jpg')), (WIDTH, HEIGHT)
)

RABBITS = []
WOLVES = []
GENOTYPE_STAT = {}
GENOTYPE_STAT_OVER_TIME = {}

class Rabbit:
    REPRODUCE_THRESOLD = 7
    DEATH_THRESOLD = 10

    def __init__(self, gene_list: dict):
        # surface object
        self.age = 0
        self.gene = Gene(gene_list)
        self.sf = pg.transform.scale(
    pg.image.load(self.gene.get_image_path()), IMAGE_SIZE)
    
    def get_blit(self):
        return (self.sf, (random.randint(*WIDTH_RANGE), random.randint(*HEIGHT_RANGE)))
    
    def get_genes(self):
        return self.gene.get_genes()
    
    def time_passed(self):
        # 0 for nothing
        # -1 for death
        # 1 for reproducing

        self.age += 1
        if self.is_dead(): return -1
        elif self.age >= Rabbit.REPRODUCE_THRESOLD: return 1
        else: return 0
    
    def is_dead(self):
        if self.age >= Rabbit.DEATH_THRESOLD:
            return True
        return False

class Gene:
    GENE_NAMES = ['Teeth', 'Speed', 'Color', 'Size', 'Time',
                  'Acromegaly', 'Metabolism', 'OxygenEffiency']
    GENOTYPE = ['AA', 'Aa', 'aa']

    def __init__(self, gene_list: dict):
        self.gene_dict = gene_list
    
    def get_genes(self):
        return self.gene_dict
    
    def get_image_path(self):
        return os.path.join('evo', 'Assets', 'new_rabbit.png')

def gene_reproduce(father_gene: dict, mother_gene: dict) -> dict:
    ret = dict()

    for name in Gene.GENE_NAMES:
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

x = []
y1 = []
y2 = []
def print_genostat(gene_name):
    s = 2*sum(GENOTYPE_STAT[gene_name].values())
    ret = (round((2*GENOTYPE_STAT[gene_name]['AA'] + GENOTYPE_STAT[gene_name]['Aa'])/s, 2),
           round((GENOTYPE_STAT[gene_name]['Aa'] + 2*GENOTYPE_STAT[gene_name]['aa'])/s, 2))
    GENOTYPE_STAT_OVER_TIME[gene_name].append(ret)

    x.append(len(GENOTYPE_STAT_OVER_TIME[gene_name]))
    y1.append(GENOTYPE_STAT_OVER_TIME[gene_name][-1][0])
    y2.append(GENOTYPE_STAT_OVER_TIME[gene_name][-1][1])

    plt.cla()
    plt.plot(x, y1, label='A')
    plt.plot(x, y2, label='a')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.pause(0.2)

def initialize_rabbit(num):
    # AA 1/4, Aa 1/2, aa 1/4
    gene_cnt = dict()
    for name in Gene.GENE_NAMES:
        gene_cnt[name] = {'AA':num//4, 'Aa':num//2, 'aa':num//4}
        GENOTYPE_STAT[name] = {'AA':0, 'Aa':0, 'aa':0}
        GENOTYPE_STAT_OVER_TIME[name] = []

    for _ in range(num):
        new_gene_dict = dict.fromkeys(Gene.GENE_NAMES)

        for name in Gene.GENE_NAMES:
            picked_genotype = Gene.GENOTYPE[pick_by_probability([gene_cnt[name][key]
                                                                for key in Gene.GENOTYPE])]
            new_gene_dict[name] = picked_genotype
            gene_cnt[name][picked_genotype] -= 1
            GENOTYPE_STAT[name][picked_genotype] += 1

        RABBITS.append(Rabbit(new_gene_dict))

def main():
    running = True
    fps = 5
    #fps_limit = 600
    clock = pg.time.Clock()

    initial_rabbit = 500
    max_rabbits = 10000
    initialize_rabbit(initial_rabbit)

    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        if len(RABBITS) >= max_rabbits or len(RABBITS) <= 1:
            running = False
        
        print('Current num of rabbits: ', len(RABBITS))
        rabbit_time_passed()
        draw_window()
        print_genostat('Teeth')
    
    pg.quit()
    plt.show()

if __name__ == '__main__':
    main()