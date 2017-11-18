# Dinamika okuzb in imunizacije

import numpy as np
import random

# nastavitve
natancnost = 1
st_iteracij, korak = 300, 10

# vhodni podatki
w1 = [0.1, 0.1, 0.1, 0.3, 0.4]


def delta(w, nat):
    koordinate = [random.randint(0, 10**nat + 1) for _ in range(len(w))]
    vsota = sum(koordinate)
    if vsota != 0:
        for k in range(len(koordinate)):
            koordinate[k] *= 1/vsota
    else:
        return np.array([0, 0, 0])
    return np.array(koordinate)
# delta je simpleks (sum_{i=1:n}x_i=1, x_i>=0 za i=1:n)


def gamma(x, matrika, nat):
    x = np.array(x)
    matrika = np.array(matrika)
    for _ in range(1000):
        y = np.array(delta(x, nat))
        if len(x) == len(y):
            z = np.array([y[i]-x[i] for i in range(len(x))])
            if np.dot(np.dot(z, matrika), x) > 0:
                return y
    return None


def s(x, matrika, nat):
    y = gamma(x, matrika, nat)
    if y is None:
        return x
    return y


def konst_del(y, x, matrika):
    matrika = np.array(matrika)
    x = np.array(x)
    y = np.array(y)
    z = np.array([y[i]-x[i] for i in range(len(x))])
    mx = np.dot(np.dot(z, matrika), x)
    my = np.dot(np.dot(z, matrika), y)
    konstanta = -mx / (my - mx)
    if my-mx < 0 and konstanta < 1:
        return konstanta
    return 1


def iteracija(x=w1, n=st_iteracij, nat=natancnost, k=korak):
    w = [x[i] / sum(x) for i in range(len(x))]

    matrika = [[0 for _ in range(len(w))] for _ in range(len(w))]
    for i in range(len(w)):
        for j in range(len(w)):
            matrika[i][j] = abs(w[i] - w[j])
    # hitrost konvergence in limita odvisna od definicije matrike A_{i,j}
    print(matrika)

    matrika = np.array(matrika)
    w = np.array(w)
    pop = w
    print('x( t={} ) = {}'.format(0, pop))
    for t in range(1, n+1):
        strategija = np.array(s(pop, matrika, nat))
        pop = np.array(pop)
        konstanta = konst_del(strategija, pop, matrika)
        pop = konstanta * (strategija-pop) + pop
        if t % k == 0:
            print('x( t={} ) = {}'.format(t, pop))
    return [w, pop]


iteracija(w1)
