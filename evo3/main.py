import pygame as pg
import matplotlib.pyplot as plt
import random
import sys
from constant import *
from animals import *
from buttons import *
from initialize import *

print = sys.stdout.write

x = list()
y1 = dict()
y2 = dict()
time = 0
FIGURE = plt.figure("Allele frequency", figsize=(6.4, 8.0))
fig = dict()
CURRENT_ENV = None

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
    draw_percentage = 1
    WINDOW.blit(BACKGROUND, (0, 0))
    
    for i in range(0, len(RABBITS), 100//draw_percentage):
        WINDOW.blit(*RABBITS[i].get_blit())
    
    '''for i in range(0, len(WOLVES), 100//draw_percentage):
        WINDOW.blit(*WOLVES[i].get_blit())'''
    
    WINDOW.fill(BLACK, BUTTON_BACKGROUND)
    for button in BUTTONS:
        if button.get_pressed() and button.get_name() == CURRENT_ENV:
            WINDOW.fill(RECT_CLICK_COLOR, button.get_rect())
        else:
            WINDOW.fill(RECT_NOCLICK_COLOR, button.get_rect())
        WINDOW.blit(button.get_text(), button.get_pos())
    
    pg.display.update()

def delete_genotype_stat(dead: list, animals: list):
    # dead is list of boolean

    for i in range(len(dead)):
        if dead[i]:
            deleted_genes_dict = animals[i].get_genes()
            (age, child) = animals[i].get_age_and_childs()
            for gene, genotype in iter(deleted_genes_dict.items()):
                GENOTYPE_STAT[gene][genotype] -= 1
                name = GENOTYPE_NAMES[gene][0] if 'A' in genotype else GENOTYPE_NAMES[gene][1]
                AGE_STAT[gene][name][0] += age
                AGE_STAT[gene][name][1] += 1
                CHILDS_STAT[gene][name][0] += child
                CHILDS_STAT[gene][name][1] += 1

def get_dead_and_reproducing(dead: list, reproducing: list, animals: list):
    for i, animal in enumerate(animals):
        ret = animal.time_passed(CURRENT_ENV)
        if ret == -1:
            dead[i] = True
        elif ret == 1:
            reproducing.append(animal)

def rabbit_time_passed():
    # 죽을 토끼를 죽이고 번식할 토끼들 중에서 무작위로 2마리씩 골라 번식시킨다.
    global RABBITS

    dead = [False] * len(RABBITS)
    reproducing_rabbits = []
    get_dead_and_reproducing(dead, reproducing_rabbits, RABBITS)
    delete_genotype_stat(dead, RABBITS)
    RABBITS = [rabbit for i, rabbit in enumerate(RABBITS) if not dead[i]]

    if len(reproducing_rabbits) <= 1: return

    cnt = 0
    already_picked = [False] * len(reproducing_rabbits)
    
    i = j = 0
    while cnt <= len(reproducing_rabbits)//2:
        # 아직 뽑히지 않은 (i, j) 쌍을 찾는다 (단, i != j)
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

'''def wolf_time_passed():
    global WOLVES

    dead = [False for _ in range(len(WOLVES))]
    reproducing = []
    get_dead_and_reproducing(dead, reproducing, WOLVES)
    WOLVES = [wolf for i, wolf in enumerate(WOLVES) if not dead[i]]

    for _ in range(len(reproducing)):
        WOLVES.append(Wolf(random.randint(*WIDTH_RANGE), random.randint(*HEIGHT_RANGE)))'''

def print_genostats(plot_print_gap: int):
    global RABBITS, time

    x.append(time)
    for gene_name in GENE_NAMES:
        s = 2*sum(GENOTYPE_STAT[gene_name].values())
        ret = (round((2*GENOTYPE_STAT[gene_name]['AA'] + GENOTYPE_STAT[gene_name]['Aa'])/s, 2),
            round((GENOTYPE_STAT[gene_name]['Aa'] + 2*GENOTYPE_STAT[gene_name]['aa'])/s, 2))

        y1[gene_name].append(ret[0])
        y2[gene_name].append(ret[1])

        if time % plot_print_gap == 0:
            fig[gene_name].cla()
            fig[gene_name].plot(x, y1[gene_name], label=GENOTYPE_NAMES[gene_name][0])
            fig[gene_name].plot(x, y2[gene_name], label=GENOTYPE_NAMES[gene_name][1])
            fig[gene_name].legend(loc='upper left')
            fig[gene_name].set_title(gene_name+' frequency')
        plt.pause(0.1)

    time += 1

'''def initialize_wolf(num):
    # num 마리의 늑대를 만든다
    global WOLVES
    
    for _ in range(num):
        WOLVES.append(Wolf(random.randint(*WIDTH_RANGE), random.randint(*HEIGHT_RANGE)))'''

'''def detect_collision():
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
    RABBITS = [rabbit for i, rabbit in enumerate(RABBITS) if not dead[i]]'''

def print_age_and_child_stats():
    calc_average = lambda x: round(x[0]/x[1], 2)
    for gene in GENE_NAMES:
        print('-'*55 + '\n')
        age_ret = [0, 0]
        child_ret = [0, 0]
        for i, name in enumerate(GENOTYPE_NAMES[gene]):
            age_ret[i] = calc_average(AGE_STAT[gene][name])
            child_ret[i] = calc_average(CHILDS_STAT[gene][name])

        if y1[gene][-1] > y2[gene][-1]:
            if age_ret[0] < age_ret[1]:
                age_ret[0], age_ret[1] = age_ret[1], age_ret[0]
            if child_ret[0] < child_ret[1]:
                child_ret[0], child_ret[1] = child_ret[1], child_ret[0]
        else:
            if age_ret[0] > age_ret[1]:
                age_ret[0], age_ret[1] = age_ret[1], age_ret[0]
            if child_ret[0] > child_ret[1]:
                child_ret[0], child_ret[1] = child_ret[1], child_ret[0]

        for i, name in enumerate(GENOTYPE_NAMES[gene]):
            print(name + '\'s average age and childs: ' + str(age_ret[i]) + ' ' + str(child_ret[i]))
            if i == 0:
                print(' / ' + str(round(y1[gene][-1], 2)) + '\n')
            else:
                print(' / ' + str(round(y2[gene][-1], 2)) + '\n')

def main():
    global CURRENT_ENV, BACKGROUND

    running = True
    paused = True
    fps = 60
    #fps_limit = 600
    clock = pg.time.Clock()

    # initial_rabbit must be multiple of 4
    initial_rabbit = 2000
    #initial_wolf = 50
    max_rabbits = 20000
    initialize_rabbit(initial_rabbit)
     #initialize_wolf(initial_wolf)
    initialize_plt(FIGURE, fig, y1, y2)
    initialize_buttons()
    draw_window()

    while running:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for button in BUTTONS:
                    if button.toggle_if_clicked(*mouse_pos):
                        if button.get_pressed():
                            CURRENT_ENV = button.get_name()
                            print(CURRENT_ENV+" selected\n")
                            BACKGROUND = pg.transform.scale(button.get_background(), (WIDTH, HEIGHT))
                        draw_window()
            elif event.type == pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_p]:
                    paused = False
        
        if len(RABBITS) >= max_rabbits or len(RABBITS) <= 1:
            running = False
        
        if not paused and CURRENT_ENV is not None:
            print('Current rabbits: '+str(len(RABBITS))+'\n')
            rabbit_time_passed()
            #wolf_time_passed()
            #detect_collision()
            draw_window()
            print_genostats(5)
    
    print_age_and_child_stats()
    pg.quit()
    plt.show()
    plt.close()
    return

if __name__ == '__main__':
    main()