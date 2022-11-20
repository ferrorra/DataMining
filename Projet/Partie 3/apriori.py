import numpy as np
import pandas as pd
from collections import Counter

# fonction qui convertis le dataset au format adapté pour l'execution de l'algo apriori
def create_data_table(df):
    # On enleve les espaces pour eviter des bugs lors de l'execution de l'algo
    for d in df["videoCategoryLabel"].unique():
        dd = d.replace(" ", "_")
        df["videoCategoryLabel"] = df["videoCategoryLabel"].replace(d, dd)

    # Pour chaque transaction (watcher) on lui associes ses items (videoCategoryLabel)
    data = dict()
    for d in df["Watcher "].unique():
        t = df.loc[df["Watcher "] == d]
        data[d] = list(set(t["videoCategoryLabel"]))

    return data

# fonction qui retourne une liste d'item dans le meme format que dans lequel ils se trouvent dans le dictionaire de base
def item_format(item):
    item_list = list(item.split("'"))
    special_characters = "[', ']"
    # les items etant stocker sours le formet ['X'] on le rend sous le format X
    item_list_format = [i for i in item_list if  i not in special_characters]
    return item_list_format

# fonction qui crée les tables C1, C2, C3,...,Ck
def create_ck_table(data, lk, k):
    c = Counter() # structure pythonique pour conter les objets

    if k == 1: # Dans le cas ou on construit C1 on récupére les items de notre dataset
        item_set = list(set(sum(data.values(), [])))
    else: # sinon on pour k >= 2 on les récupère de la table L(k-1)
        item_set = set()
        temp = list(lk)
        # on réalise des k-itemset unique en faisant des unions avec les objets de la table L(k-1)
        for i in range(0,len(temp)):
            for j in range(i+1,len(temp)):
                t = {z for z in item_format(temp[i])}.union({w for w in item_format(temp[j])})
                if(len(t) == k):
                    t = sorted(t)
                    item_set.add(str(t))
        item_set = list(item_set)

    # on compte le support de chaque k-itemset obtenue
    for i in item_set:
        c[i] = 0
        for d in data.values():
            if all(item in d for item in item_format(i)):
                c[i] += 1
    
    return c

# fonction qui crée les tables L1, L2, L3,...,Lk
def create_lk_table(data, ck, k, s):
    l = Counter()
    # On conserve uniquement les k-itemset de la table Ck qui vérifie le min support
    for i in ck:
        if(ck[i] >= s):
            l[str(i)] += ck[i]
    return l

# fonction qui permet de sauvegarder la table Lk dans l'ensemble L
def save_lk_table(lk, k):
    final = []
    for i in lk:
        i_set = set()
        for it in item_format(i):
            i_set.add(it)
        final.append(i_set)
    return final

# execution de l'algo apriori
def apriori(data,s):
    min_s = len(data) * s # calcule du minimum support
    final = [] # l'ensemble final L
    ck = Counter() # Table Ck
    lk = Counter() # Table Lk

    #On fixe la limite a 1000 pour etre sur de terminer l'execution de l'algorithme
    for k in range(1,1000):
        ck = create_ck_table(data,lk,k)
        if len(ck) == 0: # si la table Ck est vide on termine l'algo
            break

        lk = create_lk_table(data,ck,k,min_s)
        if len(lk) == 0: # si la table Lk est vide on termine l'algo
            break
        
        # On sauvegarde les k-itemset de la table Lk dans l'ensemble L
        l_items = save_lk_table(lk,k)
        for li in l_items:
            final.append(li)
    
    return final

# fonction qui combine tout les items de l'ensemble L entre eux pour obtenir toutes les combinaisons possibles
def pair_up(items):
    pairs = []
    for i in range(len(items)):
        for j in range(len(items)):
            pairs.append((items[i],items[j]))
    return pairs

# fonction qui retournes l'ensembles des régles possibles
# une régle est sous la forme {X --> Y} avec X et Y des itemset
def make_rules(items):
    rules = pair_up(items) # on récupère toutes les combinaisons d'itemset possible
    final_rules = list()

    # on filtres les combinaisons qui sont acceptables comme regles
    for r in rules :
        X = list(r[0])
        Y = list(r[1])
        # Dans le cas ou X intersection Y != {} on retire les items en commun de Y 
        for x in X:
            if x in Y:
                Y.remove(x)
        # Dans le cas ou la régle n'existe pas dèja et que l'itemset Y n'est pas vide après lui avoir
        # retiré les items commun on sauvegarde la régle
        if (X,Y) not in final_rules and len(Y) != 0:
            final_rules.append((X,Y))

    return final_rules

# fonction qui retourne les régles ayant une confiance supperieur a la confiance minimum 
# elle retourne aussi pour chaque regle sa confiance et son lift
def association_correlation_rules(data, items, min_conf):
    table = []
    rules = make_rules(items) # recupere les regles 
    min_c = min_conf * len(data.values()) # on calcule la confiance minimum

    # pour chaque regle on calcule sa confiance et on vérifie si elle est sup a la conf min
    for fr in rules:
        x, y = fr # on recupere les itemsets de la regle par exemple pour la regle {I1, I2} --> {I3, I4}
                # on obtient x = {I1, I2} et y = {I3, I4}

        xy = sum(fr,[]) # transforme la regle de {I1, I2} --> {I3, I4} a {I1, I2, I3, I4}

        count_x, count_y, count_xy = 0, 0, 0 # on initialise un compteur pour chaque itemset

        # on remet les espaces enlever au debut pour l'affichage final
        str_x, str_y = str(set(x)).replace("_", " "), str(set(y)).replace("_", " ")
        rule = str_x +" ---> "+ str_y

        # On calcule la frequence de chaque itemset dans notre dataset
        for d in data.values():
            if x[0] in d:
                count_x += 1
            if y[0] in d:
                count_y += 1
            check =  all(item in d for item in xy)
            if check:
                count_xy += 1
        
        # on calcule leur support 
        support_x = count_x / len(data.values())
        support_y = count_y / len(data.values())
        support_xy = count_xy / len(data.values())

        conf = support_xy / support_x  # On calcule la confiance de la regle 
        lift = support_xy / (support_x * support_y) # On calcule le lift de la regle

        if (conf * len(data.values()) >= min_c): # si la confiance de la regle >= min_c on la sauvegarde avec sa confiance et son lift
            table.append([rule, str(int(conf*100))+"%", "{:.2f}".format(round(support_xy, 2))])
    return table

# Version final de l'algo regroupant toute les fonctions
def algorithme_apriori(data,min_support,min_confidence):
    L = apriori(data,min_support)
    return association_correlation_rules(data, L, min_confidence)

# Retourne les conséquents (Y) de toutes les règles avec un item particulier comme antécédant (X)
def get_recommendation(item, rules):
    recomendations = []
    for r in rules :
        rule = r[0].split(" ---> ")
        X = rule[0]
        Y = rule[1]
        if X == item:
            recomendations.append(Y)
    return recomendations

if __name__ == '__main__':
    df = pd.read_excel("Dataset2_ TrendingVideosYoutube_.xlsx")

    data = create_data_table(df)

    rules = algorithme_apriori(data, 0.2, 0.2)

    pd.set_option('display.max_colwidth', None)
    print(pd.DataFrame(rules, columns = ["Rule","Confidence","Lift"]))
    
    print(get_recommendation("{'Education'}", rules))
