import numpy as np
import sys
from conversion_matrice import convertir_matrice
from functools import wraps
from time import time

def timing(f):
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
        copy_demande_sommets = demande_sommets[:]
        self.m = convertir_matrice(matrice_adjacence, copy_demande_sommets)
        self.d = copy_demande_sommets
        self.a = []

        self.sommets_visites = []
        self.frequences_attribuees = [0]*len(self.d)

        self.ordre_parcours = []
        self._dfs()
        self._calculer_liste_arretes()
    
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
        for rown, arr in enumerate(np.triu(self.m)):
            for coln, val in enumerate(arr):
                if coln > rown:
                    if val > 0:
                        self.a.append((rown, coln, val))

    def _dfs(self, node=0):
        if node not in self.ordre_parcours:
            self.ordre_parcours.append(node)
            for n, v in enumerate(self.m[node]):
                if v > 0:
                    self._dfs(node=n)

    @timing
    def solution_gloutonne(self) -> list:
        self.frequences_attribuees[0] = 1

        for current_node in self.ordre_parcours[1:]:

            freq = 0
            freq_min = []

            for n, val in enumerate(self.m[current_node]):
                if val != 0 and self.frequences_attribuees[n] != 0:
                    freq = max(freq, self.frequences_attribuees[n] + val)
                    freq_min.append(self.frequences_attribuees[n] - val)

            if min(freq_min) > 0:
                self.frequences_attribuees[current_node] = min(freq_min)
            else:
                self.frequences_attribuees[current_node] = freq

        
        return self.frequences_attribuees

    def span(self):
        return max(self.frequences_attribuees)


    def solution_gloutnne_naive(self) -> list:
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
        for sommet_a, sommet_b, valeur in self.a:
            if abs(self.frequences_attribuees[sommet_a] - self.frequences_attribuees[sommet_b]) < valeur:
                print(f"SOLUTION INVALIDE : ({sommet_a}, {sommet_b}) devrait être au minimum {valeur} mais est {abs(self.frequences_attribuees[sommet_a] - self.frequences_attribuees[sommet_b])}")
                return
        
        print("SOLUTION VALIDE")

def charger_jeu_donnees(liste_m, liste_dem):
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

    for l, m in couples:
        print("Traitement du problème L%d,M%d :" % (l+1, m+1))

        graphe = Graphe(matrices[m], demandes[l])
        frequences = graphe.solution_gloutonne()
        span = graphe.span()
        graphe.test_solution_valide()

        print("\tSpan: %d" % span)
 

    """ m4 = np.array([
        [0, 3, 0, 2, 0, 0, 0, 10],
        [3, 0, 1, 2, 0, 0, 0, 0],
        [0, 1, 3, 4, 0, 0, 0, 0],
        [2, 2, 4, 0, 8, 4, 6, 5],
        [0, 0, 0, 8, 1, 3, 0, 0],
        [0, 0, 0, 4, 3, 0, 1, 0],
        [0, 0, 0, 6, 0, 1, 2, 8],
        [10, 0, 0, 5, 0, 0, 8, 0],
    ])
    s4 = [1, 1, 3, 1, 2, 1, 5, 1]
    g4 = Graphe(m4, s4)

    f4 = g4.solution_gloutonne()
    span4 = g4.span()
    print(f4)
    g4.test_solution_valide()
    print("Span du graphe: %d" % span4) """