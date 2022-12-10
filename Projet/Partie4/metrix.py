import numpy as np 
import matplotlib.pyplot as plt

def confusion_matrix(y_true, y_pred, labels=None):
    #On obtient les classes distinctes et leurs nombres
    y_true_no_duplicate = sorted(set(y_true))
    n = len(y_true_no_duplicate)
    #On intialise la matricde de confusion
    matrix = np.zeros((n,n), dtype=np.int32)
    
    for i in range(len(y_true)):
        matrix[y_true_no_duplicate.index(y_true[i])][y_true_no_duplicate.index(y_pred[i])] += 1
    
    return matrix

def accuracy(y_true, y_pred, labels=None):
    cm = confusion_matrix(y_true, y_pred, labels)
    first_diagonal = np.diag(cm)
    columns_sum = cm.sum(axis=0)
    #Accuracy=(TP+TN)/(TP+TN+FP+FN)
    lines_sum = cm.sum(axis=1)
    matrix_sum = cm.sum(axis=(0, 1))
    return np.divide(first_diagonal,
                     matrix_sum, 
                     out = np.zeros(first_diagonal.shape[0]), 
                     where = lines_sum != 0)

def tpr_scores(y_true, y_pred, labels=None): #sensitivity
    cm = confusion_matrix(y_true, y_pred, labels)
    first_diagonal = np.diag(cm)
    columns_sum = cm.sum(axis=0)
    # les TPs  sont stoqués dans la diagonale
    tps = first_diagonal
    lines_sum = cm.sum(axis=1)
    matrix_sum = cm.sum(axis=(0, 1))
    # les FNs sont calculés par la formule :
    # = (sommes des colonnes - diagonale)
    fns = columns_sum - first_diagonal
    return np.divide(tps,
                     tps + fns, 
                     out = np.zeros(fns.shape[0]), 
                     where = lines_sum != 0)

def fnr_scores(y_true, y_pred, labels=None): 
    cm = confusion_matrix(y_true, y_pred, labels)
    first_diagonal = np.diag(cm)
    columns_sum = cm.sum(axis=0)
    # les TPs  sont stoqués dans la diagonale
    tps = first_diagonal
    lines_sum = cm.sum(axis=1)
    matrix_sum = cm.sum(axis=(0, 1))
    # les FNs sont calculés par la formule :
    # = (sommes des colonnes - diagonale)
    fns = columns_sum - first_diagonal
    return np.divide(fns,
                     tps + fns, 
                     out = np.zeros(fns.shape[0]), 
                     where = lines_sum != 0)



def fscore(y_true, y_pred, labels=None):
    #2 * (precision * recall) / (precision + recall)
    return(2*(precision_scores(y_true, y_pred, labels=None)*recall_scores(y_true, y_pred, labels=None))/(precision_scores(y_true, y_pred, labels=None)+recall_scores(y_true, y_pred, labels=None)))

def recall_scores(y_true, y_pred, labels=None):
    cm = confusion_matrix(y_true, y_pred, labels)
    # TPs de chaque classe sont stoqués dans la première diagonale
    first_diagonal = np.diag(cm)
    # les sommes TPs + FNs pour chaque classe représentent la somme des lignes
    lines_sum = cm.sum(axis=1)
    return np.divide(first_diagonal, 
                     lines_sum, 
                     out = np.zeros(first_diagonal.shape[0]), 
                     where=lines_sum!=0)


def precision_scores(y_true, y_pred, labels=None):
    cm = confusion_matrix(y_true, y_pred, labels)
    # TPs de chaque classe sont stoqués dans la première diagonale
    first_diagonal = np.diag(cm)
    # les sommes TPs + FPs pour chaque classe représentent la somme des lignes
    columns_sum = cm.sum(axis=0)
    return np.divide(first_diagonal, 
                     columns_sum, 
                     out = np.zeros(first_diagonal.shape[0]), 
                     where=columns_sum!=0)

def fpr_scores(y_true, y_pred, labels=None):
    cm = confusion_matrix(y_true, y_pred, labels)
    first_diagonal = np.diag(cm)
    columns_sum = cm.sum(axis=0)
    # les FPs représentent les sommes des colonnes 
    # moins les TPs qui sont stoqués dans la diagonale
    fps = columns_sum - first_diagonal
    lines_sum = cm.sum(axis=1)
    matrix_sum = cm.sum(axis=(0, 1))
    # les TNs sont calculés par la formule :
    # = somme matrice - TPs - FPs - FNs
    # = somme matrice - (diagonale) - (sommes des colonnes - diagonale) -(sommes des lignes - diagonale)
    # = somme matrice - sommes des colonnes - sommes des lignes + diagonale
    tns = matrix_sum - columns_sum - lines_sum + first_diagonal
    return np.divide(fps, 
                     fps + tns, 
                     out = np.zeros(fps.shape[0]), 
                     where = lines_sum != 0)



def tnr_scores(y_true, y_pred, labels=None): #specificity
    cm = confusion_matrix(y_true, y_pred, labels)
    first_diagonal = np.diag(cm)
    columns_sum = cm.sum(axis=0)
    # les FPs représentent les sommes des colonnes 
    # moins les TPs qui sont stoqués dans la diagonale
    fps = columns_sum - first_diagonal
    lines_sum = cm.sum(axis=1)
    matrix_sum = cm.sum(axis=(0, 1))
    # les TNs sont calculés par la formule :
    # = somme matrice - TPs - FPs - FNs
    # = somme matrice - (diagonale) - (sommes des colonnes - diagonale) -(sommes des lignes - diagonale)
    # = somme matrice - sommes des colonnes - sommes des lignes + diagonale
    tns = matrix_sum - columns_sum - lines_sum + first_diagonal
    return np.divide(tns,
                     fps + tns, 
                     out = np.zeros(tns.shape[0]), 
                     where = lines_sum != 0)


# Fonction de test pour calculer toutes les metriques pour une prédicition donnée
def calculate_metrics(y_true, y_pred, labels):

    recall = recall_scores(y_true, y_pred, labels=labels).mean()
    precision = precision_scores(y_true, y_pred, labels=labels).mean()
    fpr = fpr_scores(y_true, y_pred, labels=labels).mean()
    tnr = tnr_scores(y_true, y_pred, labels=labels).mean()
    tpr = tpr_scores(y_true, y_pred, labels=labels).mean()
    fnr = fnr_scores(y_true, y_pred, labels=labels).mean()
    fs = fscore(y_true, y_pred, labels=labels).mean()
    acc = accuracy(y_true, y_pred, labels=labels).mean()

    return (f"recall  :{recall} \n precision :{precision}  \n fpr  : {fpr} \n tnr  / Specificity  : {tnr}\n tpr  / Sensitivity : {tpr}\nfnr  : {fnr} \n F-score  : {fs}\n Accuracy    : {acc}\n")

    #print("recall    :", recall)
    #print("precision :", precision)
    #print("fpr       :", fpr)
    #print("tnr  / Specificity     :", tnr)
    #print("tpr  / Sensitivity     :", tpr)
    #print("fnr    :", fnr)
    #print("F-score    :", fs)
    #print("Accuracy    :", acc)

