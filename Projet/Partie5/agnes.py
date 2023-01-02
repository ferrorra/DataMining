import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import warnings
from collections import Counter
warnings.filterwarnings("ignore")

# La méthode Lien maximum est utilisée pour retouner a valeur maximale de toutes les
# distances par paires entre les éléments du cluster C1 et les éléments du cluster C2.
# 𝑑𝑖𝑠𝑡(𝐶1, 𝐶2) = 𝑀𝑎𝑥 ( 𝑑𝑖𝑠𝑡(𝑒1, 𝑒2) , 𝑒1 ∈ 𝐶1 𝑒𝑡 𝑒2 ∈ 𝐶2 ).
def complete_linkage(c1, c2):
    distances = np.zeros(len(c1) * len(c2))
    l = 0
    for i in range(len(c1)):
        for j in range(len(c2)):
            distances[l] = np.sum(np.abs(c1[i] - c2[j]))
            l += 1

    return np.amax(distances) # On retourne la valeur maximale de toutes les distances par paires entre les éléments du cluster C1 et les éléments du cluster C2

# La méthode Liaison minimale utilisée pour retouner a valeur minimale de toutes les
# distances par paires entre les éléments du cluster C1 et les éléments du cluster C2.
# 𝑑𝑖𝑠𝑡(𝐶1, 𝐶2) = 𝑀𝑖𝑛 ( 𝑑𝑖𝑠𝑡(𝑒1, 𝑒2) , 𝑒1 ∈ 𝐶1 𝑒𝑡 𝑒2 ∈ 𝐶2 ).
def single_linkage(c1, c2):
    distances = np.zeros(len(c1) * len(c2))
    l = 0
    for i in range(len(c1)):
        for j in range(len(c2)):
            distances[l] = np.sum(np.abs(c1[i] - c2[j]))
            l += 1

    return np.amin(distances) # On retourne la valeur minimale de toutes les distances par paires entre les éléments du cluster C1 et les éléments du cluster C2

# La méthode Liaison moyenne utilisée pour retouner a valeur moyenne de toutes les
# distances par paires entre les éléments du cluster C1 et les éléments du cluster C2.
# 𝑑𝑖𝑠𝑡(𝐶1, 𝐶2) = Σ(𝑒1 ∈ 𝐶1) Σ(𝑒2 ∈ 𝐶2 ) d𝑖𝑠𝑡(𝑒1, 𝑒2) / (𝑛1 * 𝑛2) où 𝑛1 et 𝑛2 sont les tailles des clusters C1 et C2.
def mean_linkage(c1, c2):
    distances = np.zeros(len(c1) * len(c2))
    l = 0
    for i in range(len(c1)):
        for j in range(len(c2)):
            distances[l] = np.sum(np.abs(c1[i] - c2[j]))
            l += 1

    return np.mean(distances) # On retourne la valeur moyenne de toutes les distances par paires entre les éléments du cluster C1 et les éléments du cluster C2

# La méthode Liaison centroid utilisée pour retouner la distance entre les centroides des deux clusters.
def centroid_linkage(c1, c2):
    centroid_c1 = np.mean(c1, axis=0)
    centroid_c2 = np.mean(c2, axis=0)
    return np.sum(np.abs(centroid_c1 - centroid_c2)) # On retourne la distance entre les centroides des deux clusters


def agglomeration_select_function(linkage):
    if linkage == 'complete':
        return complete_linkage
    elif linkage == 'single':
        return single_linkage
    elif linkage == 'average':
        return mean_linkage
    elif linkage == 'centroid':
        return centroid_linkage

# On utiliser cette pour récupérer les index des points du dataset qui sont dans les cluster
def get_instance_index(clusters, data):

    clusters_index = [] # Liste des index des points du dataset qui sont dans les clusters

    for i in range(len(clusters)):

        clusters_temp = [] # Liste temporaire des index des points du dataset qui sont dans le cluster i
        
        for j in range(len(clusters[i])):
            # On récupère l'index du point a partir du dataset
            clusters_temp.append(Counter(np.where(data == clusters[i][j])[0]).most_common(1)[0][0])
        
        clusters_index.append(np.array(list(set(clusters_temp)))) # On ajoute les index du cluster i à la liste des clusters
    
    return np.array(clusters_index)

# Fonction recréant l'algorithme de clustering hiérarchique
def agglomerative_clustering(data, nb_clusters, linkage_method):

    # On initialise les clusters avec les points du dataset (chaque point est un cluster)
    clusters = np.asarray(list(map(lambda el:np.asarray([el]), data.to_numpy())))

    # On défini la fonction de calcul de distance en fonction du type de linkage
    linkage = agglomeration_select_function(linkage_method)

    while len(clusters) != nb_clusters: # Tant qu'on a pas le nombre de clusters voulu
        # On calcule la matrice de distance entre les clusters
        distances = np.zeros((len(clusters), len(clusters)))
        
        for i in range(len(clusters)):
            for j in range(i, len(clusters)):
                if i == j: # On met la distance entre un cluster et lui même à 100000 pour qu'il ne soit pas choisi
                    distances[i][j] = 100000

                else : # On calcule la distance entre le cluster i et le cluster j
                    dist = linkage(clusters[i], clusters[j]) 
                    # On met la distance entre le cluster i et le cluster j et la distance entre le cluster j et le cluster i à la même valeur
                    distances[i][j] = dist
                    distances[j][i] = dist

        temp_dist = distances.copy() # On copie la matrice de distance pour ne pas la modifier
        temps_clusters = clusters.copy() # On copie les clusters pour ne pas les modifier
        new_clusters = [] # Liste des nouveaux clusters

        while len(temp_dist) != 0: # Tant qu'il reste des clusters
            index = np.argmin(temp_dist, axis=1)[0] # On récupère l'index du cluster le plus proche du cluster 0
            new_clusters.append(np.concatenate((temps_clusters[0], temps_clusters[index]))) # On crée le nouveau cluster en concaténant les deux clusters les plus proches

            temps_clusters = np.delete(temps_clusters, 0,  axis= 0) # On supprime le cluster 0
            temp_dist = np.delete(temp_dist , 0,  axis= 0) # On supprime la liste des distances du cluster 0
            temp_dist = np.delete(temp_dist , 0,  axis= 1) # On supprime la distance entre le cluster 0 et les autres clusters

            if index != 0: # Si le cluster le plus proche du cluster 0 n'est pas le cluster 0
                temps_clusters = np.delete(temps_clusters, index - 1,  axis= 0) # On supprime le cluster le plus proche du cluster 0
                temp_dist = np.delete(temp_dist , index - 1,  axis= 0) # On supprime la liste des distances du cluster le plus proche du cluster 0
                temp_dist = np.delete(temp_dist , index - 1,  axis= 1) # On supprime la distance entre le cluster le plus proche du cluster 0 et les autres clusters
            if len(temps_clusters) + len(new_clusters) == nb_clusters: 
                new_clusters.extend(temps_clusters)
                break
        clusters = new_clusters # On met à jour les clusters
    
    return get_instance_index(clusters, data) # On retourne les index des points du dataset qui sont dans les clusters