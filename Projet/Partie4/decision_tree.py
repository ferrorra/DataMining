import numpy as np
import pandas as pd
import random

class DT_Node:
    """
    Ceci est une classe pour représenter chaque noeud de notre arbre de décision

    Parameters:
    ----------
    val: int
        L'indice du mode des classes (pour prédire si attrition ou pas)
    
    Attributes:
    ----------
        feature_index: int
            L'indice du feature avec lequel on va split l'arbre

        threshold: float
            Notre seuil pour le split

        cost: float
            cost function to calculate impurity of each node

        left: <class DT_Node>
            coté gauche <<<<< less

        right: <class DT_Node>
            coté droit >>>>>> more
    """
    def __init__(self,val):
        self.val = val
        self.feature_index = 0
        self.threshold = 0
        self.cost = 0
        self.left = None
        self.right = None
        

class DecisionTree:
   
    """
    Modélisation de notre arbre de décision.

    Parameters
    ----------
    max_depth: int, default=None
        La profondeur de notre arbre. Si Null, on developpes notre arbre jusqu'a ce que nos feuilles aient le maximum de purity (cost ==>0).

    max_features: int, float, default=None
        Paramètre utilisé pour définir le seuil de split. Si float et <1, 
        max_features prend la taille des features dans le dataset entier.

    random_state: int, default=None
        La permutaions des features apres chaque split est aléatoire. 

    Criterion: str, default='gini'
        Fonction de cout pour notre arbre de décision

    Attributes:
    ----------
    tree: <class DT_Node>
        La racine de notre
    """
    def __init__(self,max_depth=None,max_features=None,random_state=None, criterion='gini'):
        self.max_depth = max_depth
        self.max_features = max_features #n_samples
        self.random_state = random_state
        self.criterion = criterion
        self.tree = None

    def fit(self, X, y):
        """
        Fonction d'entrainement de notre modèle.

        Parameters:
        ----------     
        X: np.array or pd.core.frame.DataFrame
            Features d'entrainement
        
        y: np.array or pd.core.series.Series
            Notre Target

        Returns:
        -------
        None
        """
        # store number of classes and features of the dataset into model object
        if isinstance(X, pd.core.frame.DataFrame):
            X = X.values
        if isinstance(y, pd.core.series.Series):
            y = y.values

        self.n_classes = len(set(y)) #définir le type de classification (binaire/ multiclass)
        self.n_features = X.shape[1] #définir le nombre des features
        if self.max_features==None: #définir le nombre de features qu'on veut utiliser pour l'entrainement
            self.max_features = self.n_features

        if isinstance(self.max_features,float) and self.max_features<=1: #si notre max_features n'est pas bien défini on le redéfini
            self.max_features = int(self.max_features*self.n_features)

        # create tree for the dataset
        self.tree = self.grow_tree(X,y,self.random_state) #on commence l'entrainement


    def predict(self,X):
        """
        Prédire la classe de plusieurs instances.

        Parameters:
        ----------     
        X: np.array or pd.core.frame.DataFrame
            Test set      

        Returns:
        -------
        predicted_classes: np.array
            Résultat des prédictions     
        """
        if isinstance(X, pd.core.frame.DataFrame):
            X = X.values

        predicted_classes = np.array([self.predict_example(inputs) for inputs in X])

        return predicted_classes


    def best_split(self, X, y, random_state):
        """
        Déterminer le feature et le seuil optimal pour effectuer notre split.

        Parameters:
        ----------     
        X: np.array
            Train.

        y: np.array
            Target.

        random_state: int, default=None

        Returns:
        -------
        best_feat_id: int, None
            Le fature le plus adéquat pour faire le split.
        
        best_threshold: float, None
            Le seuil le plus adéquat pour faire le split.
        """
        m = len(y) #taille des prédictions
        if m <= 1:
            return None, None, None 

        num_class_parent = [np.sum(y==c) for c in range(self.n_classes)] #proportion de chaque classe 
        if self.criterion=='entropy' : best_cost = self.get_entropy(num_class_parent,m)
        else: best_cost = self.get_gini(num_class_parent,m)

        if best_cost == 0:
            return None, None, None

        best_feat_id, best_threshold = None, None

        random.seed(random_state) #on utilise la fonction de seeding pour controler l'aléatoire
        feat_indices = random.sample(range(self.n_features),self.max_features) #on prend un echantillon d'indices aléatoire

        for feat_id in feat_indices: #on détermine le meilleure indice dans l'échantillon

            sorted_column = sorted(set(X[:,feat_id])) #on extraint l'échantillon du dataset
            threshold_values = [np.mean([a,b]) for a,b in zip(sorted_column,sorted_column[1:])] #seuil = moyenne / parent child

            for threshold in threshold_values:

                #on effectue notre split
                left_y = y[X[:,feat_id]<threshold]
                right_y = y[X[:,feat_id]>threshold]

                #on calcul les proportions 
                num_class_left = [np.sum(left_y==c) for c in range(self.n_classes)]
                num_class_right = [np.sum(right_y==c) for c in range(self.n_classes)]

                #notre fonction de cout
                if self.criterion=='entropy' : 
                    cost_left = self.get_entropy(num_class_left,len(left_y))
                    cost_right = self.get_entropy(num_class_right,len(right_y))
                else: 
                    cost_left = self.get_gini(num_class_left,len(left_y))
                    cost_right = self.get_gini(num_class_right,len(right_y))


                cost = (len(left_y)/m)*cost_left + (len(right_y)/m)*cost_right #calcul du cost total

                if cost < best_cost:
                    best_cost = cost
                    best_feat_id = feat_id
                    best_threshold = threshold

        return best_cost, best_feat_id, best_threshold




    def grow_tree(self, X, y, random_state, depth=0):
        """
        Fonction recursive du développement de notre arbre. Tant que le max_depth n'est pas atteint ou bien si le parent est moins 
        pure que la moyenne de la purity de ses enfants, on continue à developper l'arbre.

        Parameters:
        ----------     
        X: np.array
            Données d'entrainement.

        y: np.array
            Target.

        random_state: int, default=None 
            Nombre aléatoire.

        depth: int
            Nombre de splits pour chaque noeud.

        Returns:
        --------
        node: <class DT_Node>
            La racine de l'arbre (qui contient l'arbre en entier)
        """
        num_samples_per_class = [np.sum(y == i) for i in range(self.n_classes)] #nombre d'instances pour chaque type de classe
        predicted_class = np.argmax(num_samples_per_class) #avoir l'indice de la class dominante

        node = DT_Node(val=predicted_class) #créer une racine avec comme valeur la classe dominante

        if (self.max_depth is None) or (depth < self.max_depth): #tant que pas fin
            pur, id, thr  = self.best_split(X, y, random_state) #on continue à faire des plits

            if id is not None: 
                if random_state is not None:
                    random_state += 1

                #on split notre dataset pour developer les deux cotés de l'arbre    
                indices_left = X[:, id] < thr
                X_left, y_left = X[indices_left], y[indices_left]
                X_right, y_right = X[~indices_left], y[~indices_left]

                #on commence à remplir les paramétres de notre current node
                node.feature_index = id
                node.threshold = thr
                node.cost = pur
                #on fait la meme chose pour les deux cotés de l'arbre recursively
                node.left = self.grow_tree(X_left, y_left, random_state, depth + 1)
                node.right = self.grow_tree(X_right, y_right, random_state, depth + 1)
                

        return node      

    def get_gini(self, proportion, total):
        return (1.0 - sum((n / total) ** 2 for n in proportion)) #1-probabilité d'avoir la classe

    def get_entropy(self, proportion, total):
        return np.sum(-(n / total)*np.log2((n/total)+1e-9) for n in proportion)

    def predict_example(self, inputs):
        """
        Gnérer une prédiction sur une instance selon le feature est l'indice stocké dans les noeuds.

        Parameters:
        ----------     
        inputs: Une instance (ligne).

        Returns:
        --------
        node.predicted_class: int
            Notre prédiction.
        """
        node = self.tree
        #parcours simple d'un arbre
        while node.left:
            if inputs[node.feature_index] < node.threshold:
                node = node.left
            else:
                node = node.right

        return node.val     



    