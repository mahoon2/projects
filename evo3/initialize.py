import matplotlib.pyplot as plt
from constant import *
from animals import *
from buttons import *

def initialize_plt(FIGURE, fig, y1, y2):
    for i, gene_name in enumerate(GENE_NAMES):
        fig[gene_name] = FIGURE.add_subplot(3, 1, i+1, xlabel='time', ylabel='frequency')
        y1[gene_name] = list()
        y2[gene_name] = list()

    FIGURE.tight_layout()

def initialize_rabbit(num):
    # AA 1/4, Aa 1/2, aa 1/4 의 비율로 num 마리의 토끼를 만든다
    # GENOTYPE_STAT을 초기화한다(key를 설정하고 value를 0으로)
    # AGE_STAT, CHILDS_STAT을 초기화한다(key를 설정하고 value를 [sum, num]의 list로)

    gene_cnt = dict()
    for gene_name in GENE_NAMES:
        gene_cnt[gene_name] = {'AA':num//4, 'Aa':num//2, 'aa':num//4}
        GENOTYPE_STAT[gene_name] = {'AA':0, 'Aa':0, 'aa':0}
        AGE_STAT[gene_name] = {GENOTYPE_NAMES[gene_name][0]:[0, 0], GENOTYPE_NAMES[gene_name][1]:[0, 0]}
        CHILDS_STAT[gene_name] = {GENOTYPE_NAMES[gene_name][0]:[0, 0], GENOTYPE_NAMES[gene_name][1]:[0, 0]}

    for _ in range(num):
        new_gene_dict = dict.fromkeys(GENE_NAMES)

        for gene_name in GENE_NAMES:
            temp = [gene_cnt[gene_name][key] for key in GENOTYPE]
            temp_idx = {item: idx for idx, item in enumerate(temp)}
            picked_genotype = GENOTYPE[temp_idx[random.choices(temp, weights=temp)[0]]]
            new_gene_dict[gene_name] = picked_genotype
            gene_cnt[gene_name][picked_genotype] -= 1
            GENOTYPE_STAT[gene_name][picked_genotype] += 1

        RABBITS.append(Rabbit(new_gene_dict, random.randint(*WIDTH_RANGE), random.randint(*HEIGHT_RANGE)))

def initialize_buttons():
    for i, env_name in enumerate(ENV_NAMES):
        BUTTONS.append(Button(i*WIDTH//6+PADDING, PADDING, WIDTH//6-PADDING, HEIGHT//10-PADDING, env_name))