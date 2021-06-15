import numpy as np

class Graphe():
    def __init__(self, matrice_adjacence, demande_sommets) -> None:
        self.m = matrice_adjacence
        self.d = demande_sommets
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

    def solution_gloutonne(self) -> list:
        self.frequences_attribuees[0] = 1

        for current_node in self.ordre_parcours[1:]:
            print("Noeud %d" % current_node)

            freq = 0
            freq_min = []

            for n, val in enumerate(self.m[current_node]):
                if val != 0 and self.frequences_attribuees[n] != 0:
                    print("voisin %d (%d) - contrainte %d" % (n, self.frequences_attribuees[n], val))
                    freq = max(freq, self.frequences_attribuees[n] + val)
                    freq_min.append(self.frequences_attribuees[n] - val)

            if min(freq_min) > 0:
                self.frequences_attribuees[current_node] = min(freq_min)
                print("Attrribution de la fréquence MIN : %d" % min(freq_min))
            else:
                self.frequences_attribuees[current_node] = freq
                print("Attrribution de la fréquence MAX : %d" % freq)

        
        return self.frequences_attribuees


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




if __name__ == '__main__':
    m2 = np.array([
        [0, 3, 0, 3],
        [3, 0, 3, 0],
        [0, 3, 0, 3],
        [3, 0, 3, 0],
    ])
    s2 = np.array([1, 1, 1, 1])
    g2 = Graphe(m2, s2)

    #f = g2.glouton()
    #print(f)

    m3 = np.array([
        [0, 2, 0, 0, 9],
        [2, 0, 1, 0, 4],
        [0, 1, 0, 3, 0],
        [0, 0, 3, 0, 5],
        [9, 4, 0, 5, 0]
    ])
    s3 = np.array([1, 1, 1, 1, 1])

    g3 = Graphe(m3, s3)

    #f3 = g3.solution_gloutonne()
    #print("Fréquences attribuées : ", f3)
    #g3.test_solution_valide()

    m4 = np.array([
        [0, 3, 0, 2, 0, 0, 0, 10],
        [3, 0, 1, 2, 0, 0, 0, 0],
        [0, 1, 0, 4, 0, 0, 0, 0],
        [2, 2, 4, 0, 8, 4, 6, 5],
        [0, 0, 0, 8, 0, 3, 0, 0],
        [0, 0, 0, 4, 3, 0, 1, 0],
        [0, 0, 0, 6, 0, 1, 0, 8],
        [10, 0, 0, 5, 0, 0, 8, 0],
    ])
    s4 =np.array([1, 1, 1, 1, 1, 1, 1, 1])

    g4 = Graphe(m4, s4)

    print(g4.ordre_parcours)

    f4 = g4.solution_gloutonne()

    print(f4)

    g4.test_solution_valide()