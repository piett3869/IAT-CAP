import numpy as np

class Graphe():
    def __init__(self, matrice_adjacence, demande_sommets) -> None:
        self.m = matrice_adjacence
        self.d = demande_sommets
        self.a = []

        self.sommets_visites = []
        self.frequences_attribuees = [1]*len(self.d)

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
                    print(f"({rown}, {coln}) : {val}")
                    if val > 0:
                        self.a.append((rown, coln, val))

    def solution_gloutnne_naive(self) -> None:
        premier_sommet = self.a[0][0]
        self.sommets_visites.append(premier_sommet)

        for arrete in self.a:
            print(f"Parcours de l'arrête ({arrete[0]}, {arrete[1]}): {arrete[2]}")
            sommet_a, sommet_b, valeur = arrete

            if sommet_b in self.sommets_visites:
                print("SAUTE")
                if abs(self.frequences_attribuees[sommet_a] - self.frequences_attribuees[sommet_b]) >= valeur:
                    print("TOUT VA BIEN")
                    continue
                else:
                    print("TOUT NE VA PAS BIEN")


            freq_inf = self.frequences_attribuees[sommet_b] = self.frequences_attribuees[sommet_a] - valeur
            freq_sup = self.frequences_attribuees[sommet_b] = self.frequences_attribuees[sommet_a] + valeur

            self.frequences_attribuees[sommet_b] = 1 if freq_inf > 0 else freq_sup

            self.sommets_visites.append(sommet_b)
            print(f"Attribution de la fréquence {self.frequences_attribuees[sommet_a] + valeur} au sommet {sommet_b}")

        return self.frequences_attribuees



if __name__ == '__main__':
    m2 = np.array([
        [0, 3, 0, 3],
        [3, 0, 3, 0],
        [0, 3, 0, 3],
        [3, 0, 3, 0],
    ])
    s2 = np.array([1, 1, 1, 1])
    g2 = Graphe(m2, s2)
    print(g2)

    #f = g2.glouton()
    #print(f)

    m3 = np.array([
        [0, 2, 0, 0, 4],
        [0, 0, 1, 0, 4],
        [0, 0, 0, 3, 0],
        [0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0]
    ])
    s3 = np.array([1, 1, 1, 1, 1])

    g3 = Graphe(m3, s3)
    f2 = g3.solution_gloutnne_naive()
    print(f2)
