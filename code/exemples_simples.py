import numpy as np
import sys
from conversion_matrice import convertir_matrice
from functools import wraps
from time import time
import sys

def timing(f):
    """
    Wrapper pour timer les appels de fonction
    """
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te-ts))
        return result
    return wrap

class Graphe():
    def __init__(self, matrice_adjacence, demande_sommets) -> None:
        """Génère un objet Graphe sur lequel exécuter les algorithmes

        Args:
            matrice_adjacence (np.array): Matrice d'adjacence du graphe
            demande_sommets (list): Liste de la demande de chaque sommet
        """

        copy_demande_sommets = demande_sommets[:] # Copie de la liste pour éviter de modifier l'originale
        self.m = convertir_matrice(matrice_adjacence, copy_demande_sommets) # Matrice d'adjacence convertie
        self.d = copy_demande_sommets # Demande des sommets
        self.a = [] # Liste des arrêtes 2 à 2 avec leur contrainte associée

        self.sommets_visites = [] # Liste des sommets visités pour le DFS
        self.frequences_attribuees = [0]*len(self.d) # Liste des fréquences attribuées. 0 = pas de fréquence

        self.ordre_parcours = [] # Ordre de parcours DFS
        self._dfs()
        self._calculer_liste_arretes()

        self.span_glouton = 0
    
    def __str__(self) -> str:
        rep = 'Graphe:\n'
        blank = '   '*len(self.d) + '  '
        for line in self.m:
            rep += blank + ' '.join(['%3s' % str(l) for l in line]) + '\n'
        rep += ' '.join(['%3s' % str(d) for d in self.d])
        rep += '\n'
        rep += '\n'.join([f"({rown}, {coln}) : {v}" for rown, coln, v in self.a])
        return rep

    def _calculer_liste_arretes(self) -> None:
        """Construction de la liste des arrêtes 2 à 2 du graphe
        """
        for rown, arr in enumerate(np.triu(self.m)):
            for coln, val in enumerate(arr):
                if coln > rown:
                    if val > 0:
                        self.a.append((rown, coln, val))

    def _dfs(self, node=0):
        """Construction du parcours DFS du graphe

        Args:
            node (int, optional): Noeud de départ. Defaults to 0.
        """
        if node not in self.ordre_parcours:
            self.ordre_parcours.append(node)
            for n, v in enumerate(self.m[node]):
                if v > 0:
                    self._dfs(node=n)
    
    def calculer_frequences_possibles_set(self, node, span_max) -> list:
        """Pour le noeud en question, calcul de la liste des fréquences possibles en fonction du span max et des voisins

        Args:
            node (int): Noeud dont on veut connaître la liste des fréquences possibles
            span_max (int): Maximum du span

        Returns:
            list: Liste des fréquences possibles
        """
        frequences_possibles = set(range(1, span_max+1))
        frequences_impossibles = set()
        # On utilise des sets pour pouvoir utiliser les opérations d'union et de différence

        for neighbor, val in enumerate(self.m[node]):
            freq_neighbor = int(self.frequences_attribuees[neighbor])
            if val != 0 and freq_neighbor != 0:
                frequences_impossibles = frequences_impossibles.union(range(int(freq_neighbor - val + 1), int(freq_neighbor + val - 1) + 1))
        solutions = list(frequences_possibles - frequences_impossibles)
        solutions.sort()

        return solutions

    def calculer_frequences_possibles(self, node, span_max) -> list:
        """Version 1 de la méthode, en n'utilisant pas de sets

        Args:
            node (int): Noeud dont on veut connaître la liste des fréquences possibles
            span_max (int): Maximum du span

        Returns:
            list: Liste des fréquences possibles
        """

        constraints_up, ensemble_up = [], []
        constraints_down, ensemble_down = [], []
        for neighbor, val in enumerate(self.m[node]):
            if val != 0 and self.frequences_attribuees[neighbor] != 0:
                constraints_up.append(self.frequences_attribuees[neighbor] + val)
                constraints_down.append(self.frequences_attribuees[neighbor] - val)

        c_up = int(max(constraints_up))
        c_down = int(min(constraints_down))

        if c_down > 0:
            ensemble_down = list(range(1, c_down+1))
        
        if c_up < span_max:
            ensemble_up = list(range(c_up, span_max+1))

        return ensemble_down + ensemble_up


    @timing
    def solution_gloutonne(self) -> list:
        """Résout le graphe en utilisant une solution gloutonne

        Returns:
            list: Liste des fréquences attribuées aux noeuds
        """
        self.frequences_attribuees[0] = 1

        for current_node in self.ordre_parcours[1:]:

            freq = 0
            freq_min = []

            for n, val in enumerate(self.m[current_node]):
                if val != 0 and self.frequences_attribuees[n] != 0:
                    freq = int(max(freq, self.frequences_attribuees[n] + val))
                    freq_min.append(self.frequences_attribuees[n] - val)

            if min(freq_min) > 0:
                self.frequences_attribuees[current_node] = int(min(freq_min))
            else:
                self.frequences_attribuees[current_node] = freq

        
        return self.frequences_attribuees

    def solution_retour_sur_trace(self):
        """Résout le problème d'attribution des fréquences en utilisant un retour sur trace

        Args:
            span_max (int): Span max autorisé pour la coloration

        Returns:
            list or False: Liste des fréquences attribuées au noeud. Faux si pas de solution trouvée
        """
        self.frequences_attribuees = [0]*len(self.d)
        self.solution_gloutonne()
        self.span_glouton = self.span()

        print("Le span max est : %d" % self.span_glouton)

        self.frequences_attribuees = [0]*len(self.d)
        retval = self._solution_retour_sur_trace(node_index=0, span_max=self.span_glouton)

        if retval:
            return self.frequences_attribuees
        else:
            print("Pas de solution trouvée")
            return False
    
    def _solution_retour_sur_trace(self, node_index, span_max):
        """Méthode cachée appelée par la fonction du dessus, qui implémente la vraie logique du retour sur trace

        Args:
            node_index (int): index du noeud (dans l'ordre de parcours DFS) à colorer
            span_max (int): span max autorisé pour colorer le graphe

        Returns:
            bool: Vrai si on a terminé de colorer le graphe de manière valide, Faux sinon
        """

        if node_index == len(self.d):
            print("Fin de parcours")
            return self.test_solution_valide()
        
        node = self.ordre_parcours[node_index]
        
        print("(%02d/%02d) Traitement du noeud %d" % (node_index, len(self.d),  node))

        frequences_possibles = self.calculer_frequences_possibles_set(node, span_max)
        print("Fréquences possibles : ", frequences_possibles)

        for frequence in frequences_possibles:
            self.frequences_attribuees[node] = frequence
            print("Attribution de la fréquence %d au noeud %d" % (frequence, node))
            if self._solution_retour_sur_trace(node_index + 1, span_max):
                return True
            self.frequences_attribuees[node_index] = 0

        return False

    def span(self):
        """Retourne le span du graphe

        Returns:
            int: Le span du graphe
        """
        print(self.frequences_attribuees)
        return int(max(self.frequences_attribuees))

    def solution_gloutonne_naive(self) -> list:
        """Solution gloutonne pas vraiment gloutonne. Version 1

        Returns:
            list: Liste des fréquences attribuées
        """
        premier_sommet = self.a[0][0]
        self.sommets_visites.append(premier_sommet)

        for arrete in self.a:
            print(f"Parcours de l'arrête ({arrete[0]}, {arrete[1]}): {arrete[2]}")
            sommet_a, sommet_b, valeur = arrete

            if sommet_b in self.sommets_visites:
                print("Arrête déjà traitée. Vérification")
                if abs(self.frequences_attribuees[sommet_a] - self.frequences_attribuees[sommet_b]) >= valeur:
                    continue

            freq_inf = self.frequences_attribuees[sommet_a] - valeur
            freq_sup = self.frequences_attribuees[sommet_a] + valeur

            self.frequences_attribuees[sommet_b] = 1 if freq_inf > 0 else freq_sup

            self.sommets_visites.append(sommet_b)
            print(f"Attribution de la fréquence {self.frequences_attribuees[sommet_a] + valeur} au sommet {sommet_b}")

        return self.frequences_attribuees

    def test_solution_valide(self):
        """Teste si la solution trouvée respecte bien toutes les contraintes

        Returns:
            bool: Vrai ou Faux si le graphe est valide ou pas
        """ 
        for sommet_a, sommet_b, valeur in self.a:
            if abs(self.frequences_attribuees[sommet_a] - self.frequences_attribuees[sommet_b]) < valeur:
                print(f"SOLUTION INVALIDE : ({sommet_a}, {sommet_b}) devrait être au minimum {valeur} mais est {abs(self.frequences_attribuees[sommet_a] - self.frequences_attribuees[sommet_b])}")
                return False
        
        print("SOLUTION VALIDE")
        return True

def charger_jeu_donnees(liste_m, liste_dem):
    """Charge les jeux de données de l'énoncé
    """
    matrices = []
    demandes = []

    for fichier in liste_m:
        with open(fichier, 'r', encoding='utf-8') as fd:
            matrice = [[int(c) for c in r.strip().split()] for r in fd.readlines()]
    
        matrice_np = np.array(matrice)
        matrices.append(matrice_np)

    with open(liste_dem, 'r', encoding='utf_8') as fd:
        demandes = [[int(c) for c in r.strip().split()] for r in fd.readlines()]

    return matrices, demandes

if __name__ == '__main__':
    # Charger le jeu de données demandé dans le sujet

    matrices, demandes = charger_jeu_donnees(["m1.txt", "m2.txt", "m3.txt"], "dem.txt")

    couples = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (2, 0),
        (2, 1),
        (3, 0),
        (0, 2),
        (4, 1)
    ]

    sys.setrecursionlimit(10**6)

    """
    for l, m in couples:
        print("Traitement du problème L%d,M%d :" % (l+1, m+1))

        graphe = Graphe(matrices[m], demandes[l])
        frequences = graphe.solution_gloutonne()
        span = graphe.span()
        graphe.test_solution_valide()

        print("\tSpan: %d" % span)
    """

    l, m = 0, 0

    print("Traitement du problème L%d,M%d :" % (l+1, m+1))
    graphe = Graphe(matrices[m], demandes[l])
    frequences = graphe.solution_retour_sur_trace()
    span = graphe.span()
    graphe.test_solution_valide()
    print("Span glouton : %d, span backtrace : %d" % (graphe.span_glouton, span))

    # Matrice simple de l'exemple 3
    """
    m3 = np.array([
        [2, 1, 0, 0, 1],
        [1, 2, 1, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 1, 2, 1],
        [1, 0, 0, 1, 2]
    ])

    s3 = [2, 2, 2, 2, 2]

    g3 = Graphe(m3, s3)

    f3_b = g3.solution_retour_sur_trace()
    print(f3_b)
    span3 = g3.span()
    print("Span du graphe: %d" % span3)
    """

    """
    m4 = np.array([
        [0, 3, 0, 2, 0, 0, 0, 10],
        [3, 0, 1, 2, 0, 0, 0, 0],
        [0, 1, 3, 4, 0, 0, 0, 0],
        [2, 2, 4, 0, 8, 4, 6, 5],
        [0, 0, 0, 8, 1, 3, 0, 0],
        [0, 0, 0, 4, 3, 0, 1, 0],
        [0, 0, 0, 6, 0, 1, 2, 8],
        [10, 0, 0, 5, 0, 0, 8, 0],
    ], dtype=np.int16)
    s4 = [1, 1, 3, 1, 2, 1, 5, 1]
    g4 = Graphe(m4, s4)

    f4 = g4.solution_retour_sur_trace()
    span4 = g4.span()
    print(f4)
    print("Span du graphe: %d" % span4)
    g4.test_solution_valide()
    """
