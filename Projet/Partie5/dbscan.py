import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import warnings
from collections import Counter
warnings.filterwarnings("ignore")


# Retourner tous les points du dataset qui sont à une distance inférieure à eps de notre instance
def region_query(distances, i, eps):
    doc_indexes = np.where(distances[i] <= eps)[0] # On récupère les index des points qui sont à une distance inférieure à eps
    return [i for i in doc_indexes] # On retourne la liste des index des points

# Fonction qui permet de récursivement ajouter les points voisins à notre cluster
def expand_cluster(distances, document_cluster, clusters, C, neighbors, eps, min_pts):
    while len(neighbors)!=0: # Tant qu'il y a des voisins
        index_doc = neighbors.pop() # On récupère le premier voisin
        if document_cluster[index_doc] >=0 : continue # Si le point appartient déjà à un cluster et n'est pas du bruit, on passe au suivant
        document_cluster[index_doc] = C # On change la valeur -1 par le numéro du cluster pour indiquer que le point appartient à ce cluster
        clusters[C].append(index_doc) # On ajoute le point au cluster
        new_neighbors = region_query(distances,index_doc,eps) # On récupère les points voisins du point
        if len(new_neighbors)>= min_pts: neighbors.extend(new_neighbors) # Si le point a assez de voisins, on ajoute les voisins au cluster

# Fonction recréant l'algorithme DBSCAN
def dbscan(distances, eps, min_pts):
    # On itilisalise une liste a -1 pour chaque point du dataset (on ne connait pas encore son cluster)
    document_cluster = np.full(len(distances), (-1), dtype = np.int)
    clusters = [[]]
    noise = []
    C = 0
    for index_doc in range(len(distances)):
        if document_cluster[index_doc] != -1 : continue # Si le point appartient déjà à un cluster, on passe au suivant
        
        neighbors = region_query(distances,index_doc,eps) # On récupère les points voisins
        
        if len(neighbors) >= min_pts: # Si le point a assez de voisins, on crée un nouveau cluster
            document_cluster[index_doc] = C # On change la valeur -1 par le numéro du cluster pour indiquer que le point appartient à ce cluster
            clusters[C].append(index_doc) # On ajoute le point au cluster
            expand_cluster(distances, document_cluster, clusters, C, neighbors, eps, min_pts) # On ajoute les voisins du point au cluster
            C += 1 # On passe au cluster suivant
            clusters.append([])  # On initialise le nouveau cluster
        else : # Si le point n'a pas assez de voisins, on le considère comme du bruit
            document_cluster[index_doc] = -2 # On change la valeur -1 par -2 pour indiquer que le point est du bruit
            noise.append(index_doc) # On ajoute le point au bruit

            
    del clusters[C] # On supprime le dernier cluster qui est vide
    
    return clusters, noise