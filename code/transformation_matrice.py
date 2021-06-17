import numpy as np

m = np.array([
    [3, 1, 0, 3],
    [1, 6, 2, 0],
    [0, 2, 0, 4],
    [3, 0, 4, 0],
])

d = [2, 4, 1, 1]

def eclater_matrice(m, d, nsommet):
    demande_sommet = d[nsommet]
    contrainte_sommet = m[nsommet][nsommet]

    d.pop(nsommet)
    d[nsommet:nsommet] = [1] * demande_sommet

    replacement = np.ones((demande_sommet, demande_sommet)) * contrainte_sommet
    np.fill_diagonal(replacement, 0)

    nw_matrix = m[:nsommet,:nsommet]
    ne_matrix = m[:nsommet,nsommet+1:]
    sw_matrix = m[nsommet+1:,:nsommet]
    se_matrix = m[nsommet+1:,nsommet+1:]

    row_before = m[nsommet,:nsommet]
    col_before = m[:nsommet,nsommet]

    row_after = m[nsommet, nsommet+1:]
    col_after = m[nsommet+1:,nsommet]

    row_before_processed = np.tile(row_before.flatten(), (demande_sommet, 1))
    col_before_processed = np.transpose(np.tile(col_before.flatten(), (demande_sommet, 1)))

    row_after_processed = np.tile(row_after.flatten(), (demande_sommet, 1))
    col_after_processed = np.transpose(np.tile(col_after.flatten(), (demande_sommet, 1)))

    row_1 = np.hstack((nw_matrix, col_before_processed, ne_matrix))
    row_2 = np.hstack((row_before_processed, replacement, row_after_processed))
    row_3 = np.hstack((sw_matrix, col_after_processed, se_matrix))

    return np.vstack(((row_1, row_2, row_3)))

def sommets_a_etendre(m, d):
    for k_s, v_s in enumerate(d):
        if v_s > 1 and m[k_s][k_s] > 0:
            return k_s
    
    return None

print(m)
print(d)

print("===================================================")

while True:
    sommet_a_etendre = sommets_a_etendre(m, d)

    if sommet_a_etendre is not None:
        m = eclater_matrice(m, d, sommet_a_etendre)
    else:
        break

print(m)
print(d)
