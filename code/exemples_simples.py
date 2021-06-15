import numpy as np

class Graphe():
    def __init__(self, matrice_adjacence, demande_sommets) -> None:
        self.m = matrice_adjacence
        self.d = demande_sommets
        self.a = []

        self.sommets_visites = []

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


if __name__ == '__main__':
    m1 = np.array([
        [0, 3, 3], 
        [3, 0, 3], 
        [3, 3, 0]
    ])
    s1 = np.array([1, 1, 1])
    g1 = Graphe(m1, s1)
    # print(g1)

    m2 = np.array([
        [0, 3, 0, 3],
        [3, 0, 3, 0],
        [0, 3, 0, 3],
        [3, 0, 3, 0],
    ])
    s2 = np.array([1, 1, 1, 1])
    g2 = Graphe(m2, s2)
    print(g2)
