import numpy as np

def eclater_matrice(m, d, nsommet):
    """
    Découpe le sommet n° `nsommet` dans la matrice `m` en fonction de la demande `d`

    Retourne la matrice `m` et modifie le tableau `d`
    """
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
    """
    Retourne le prochain sommer à découper, ou None sinon
    """
    for k_s, v_s in enumerate(d):
        if v_s > 1 and m[k_s][k_s] > 0:
            return k_s
    
    return None

def convertir_matrice(m, d):
    """
    Convertit la matrice m (représentant les arrêtes) en prenant en compte le tableau d de demandes par sommet

    Retourne la matrice `m` et modifie le tableau `d`
    """
    while True:
        sommet_a_etendre = sommets_a_etendre(m, d)

        if sommet_a_etendre is not None:
            m = eclater_matrice(m, d, sommet_a_etendre)
        else:
            break
    
    return m
