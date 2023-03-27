import pygame as pg
import matplotlib.pyplot as plt
import random
import sys
from constant import *
from animals import *

print = sys.stdout.write

def gene_reproduce(father_gene: dict, mother_gene: dict) -> dict:
    ret = dict()

    for name in GENE_NAMES:
        temp1 = father_gene[name]
        temp2 = mother_gene[name]
        ret[name] = random.choice(temp1) + random.choice(temp2)
        if ret[name] == 'aA':
            ret[name] = 'Aa'
    
    return ret

def draw_window():
    # Only approximately 'draw_percentage'% animals will be drawn 
    draw_percentage = 10
    WINDOW.blit(BACKGROUND, (0, 0))
    
    for i in range(0, len(RABBITS), 100//draw_percentage):
        WINDOW.blit(*RABBITS[i].get_blit())
    
    for i in range(0, len(WOLVES), 100//draw_percentage):
        WINDOW.blit(*WOLVES[i].get_blit())
    
    pg.display.update()

def delete_genotype_stat(dead: list, animals: list):
    # dead is list of boolean

    for i in range(len(dead)):
        if dead[i]:
            deleted_genes_dict = animals[i].get_genes()
            for gene, genotype in iter(deleted_genes_dict.items()):
                GENOTYPE_STAT[gene][genotype] -= 1

def get_dead_and_reproducing(dead: list, reproducing: list, animals: list):
    for i, animal in enumerate(animals):
        ret = animal.time_passed()

        if ret == -1:
            dead[i] = True
        elif ret == 1:
            reproducing.append(animal)

def rabbit_time_passed():
    # 죽을 토끼를 죽이고 번식할 토끼들 중에서 무작위로 2마리씩 골라 번식시킨다.
    global RABBITS

    dead = [False for _ in range(len(RABBITS))]
    reproducing_rabbits = []
    get_dead_and_reproducing(dead, reproducing_rabbits, RABBITS)
    delete_genotype_stat(dead, RABBITS)
    RABBITS = [rabbit for i, rabbit in enumerate(RABBITS) if not dead[i]]

    if len(reproducing_rabbits) <= 1: return

    cnt = 0
    already_picked = [False for _ in range(len(reproducing_rabbits))]
    
    i = j = 0
    while cnt <= len(reproducing_rabbits)//2:
        while already_picked[i]:
            i = random.randint(0, len(reproducing_rabbits)-1)
        while already_picked[j] and i == j:
            j = random.randint(0, len(reproducing_rabbits)-1)

        new_gene_dict = gene_reproduce(reproducing_rabbits[i].get_genes(),
                                       reproducing_rabbits[j].get_genes())
        
        for gene, genotype in iter(new_gene_dict.items()):
            GENOTYPE_STAT[gene][genotype] += 1

        RABBITS.append(Rabbit(new_gene_dict, random.randint(*WIDTH_RANGE), random.randint(*HEIGHT_RANGE)))
        already_picked[i] = already_picked[j] = True
        cnt += 2

def wolf_time_passed():
    global WOLVES

    dead = [False for _ in range(len(WOLVES))]
    reproducing = []
    get_dead_and_reproducing(dead, reproducing, WOLVES)
    WOLVES = [wolf for i, wolf in enumerate(WOLVES) if not dead[i]]

    for _ in range(len(reproducing)):
        WOLVES.append(Wolf(random.randint(*WIDTH_RANGE), random.randint(*HEIGHT_RANGE)))

x = dict.fromkeys(GENE_NAMES, list())
y1 = dict.fromkeys(GENE_NAMES, list())
y2 = dict.fromkeys(GENE_NAMES, list())
time = 0

def print_genostat(gene_name):
    global RABBITS

    s = 2*sum(GENOTYPE_STAT[gene_name].values())
    if s != 2*len(RABBITS):
        print(s + '\n')
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
    # AA 1/4, Aa 1/2, aa 1/4 의 비율로 num 마리의 토끼를 만든다
    # GENOTYPE_STAT을 초기화한다(key를 설정하고 value를 0으로)

    gene_cnt = dict()
    for name in GENE_NAMES:
        gene_cnt[name] = {'AA':num//4, 'Aa':num//2, 'aa':num//4}
        GENOTYPE_STAT[name] = {'AA':0, 'Aa':0, 'aa':0}

    for _ in range(num):
        new_gene_dict = dict.fromkeys(GENE_NAMES)

        for name in GENE_NAMES:
            temp = [gene_cnt[name][key] for key in GENOTYPE]
            temp_idx = {item: idx for idx, item in enumerate(temp)}
            picked_genotype = GENOTYPE[temp_idx[random.choices(temp, weights=temp)[0]]]
            new_gene_dict[name] = picked_genotype
            gene_cnt[name][picked_genotype] -= 1
            GENOTYPE_STAT[name][picked_genotype] += 1

        RABBITS.append(Rabbit(new_gene_dict, random.randint(*WIDTH_RANGE), random.randint(*HEIGHT_RANGE)))

def initialize_wolf(num):
    # num 마리의 늑대를 만든다
    global WOLVES
    
    for _ in range(num):
        WOLVES.append(Wolf(random.randint(*WIDTH_RANGE), random.randint(*HEIGHT_RANGE)))

def detect_collision():
    global RABBITS

    dead = [False for _ in range(len(RABBITS))]
    rabbits_pos = [rabbit.get_pos() for rabbit in RABBITS]
    wolf_margin = 7

    cnt = 0
    for wolf in WOLVES:
        wp = wolf.get_pos()

        for i, pos in enumerate(rabbits_pos):
            if wp[0]-wolf_margin <= pos[0] <= wp[0]+wolf_margin and\
            wp[1]-wolf_margin <= pos[1] <= wp[1]+wolf_margin and not dead[i]:
                dead[i] = True
                wolf.eat()
                cnt += 1
    
    print(str(cnt)+' rabbits eaten!'+'\n')
    delete_genotype_stat(dead, RABBITS)
    RABBITS = [rabbit for i, rabbit in enumerate(RABBITS) if not dead[i]]

def main():
    running = True
    paused = True
    fps = 60
    #fps_limit = 600
    clock = pg.time.Clock()

    draw_window()
    # initial_rabbit must be multiple of 4
    initial_rabbit = 1000
    initial_wolf = 50
    max_rabbits = 2000
    initialize_rabbit(initial_rabbit)
    initialize_wolf(initial_wolf)

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
            print('Current rabbits and wolves: '+str(len(RABBITS))+' '+str(len(WOLVES))+'\n')
            rabbit_time_passed()
            wolf_time_passed()
            detect_collision()
            draw_window()

            CURRENT_ENV["Food type"] = 0
            print_genostat("Teeth")
            '''for gene_name in GENE_NAMES:
                print_genostat(gene_name)'''
    
    plt.show()
    pg.quit()

if __name__ == '__main__':
    main()