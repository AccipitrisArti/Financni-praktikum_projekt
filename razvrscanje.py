# Dinamika okuzb in imunizacije

import numpy as np
import random


def delta(w, nat):
    vsota = 0
    koordinate = [0 for _ in range(len(w))]
    while vsota == 0:
        koordinate = [random.randint(0, 10**nat + 1) for _ in range(len(w))]
        vsota = sum(koordinate)
    for k in range(len(koordinate)):
        koordinate[k] *= 1/vsota
    return np.array(koordinate)
# delta je simpleks (sum_{i=1:n}x_i=1, x_i>=0 za i=1:n)


def gamma(x, matrika, nat):
    x = np.array(x)
    matrika = np.array(matrika)
    for _ in range(10000):
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
    if -1e-16 < my - mx:    # abs(my - mx) < 1e-16 and my - mx > 0
        return 1
    konstanta = - mx / (my - mx)
    if konstanta < 1:
        return konstanta
    return 1


def iteracija(x, n, nat):
    w = [x[i] / sum(x) for i in range(len(x))]

    matrika = [[0 for _ in range(len(w))] for _ in range(len(w))]
    for i in range(len(w)):
        for j in range(len(w)):
            matrika[i][j] = abs(w[i] - w[j])
    # hitrost konvergence in limita odvisna od definicije matrike A_{i,j}
    # A je matrika izplacil (koristnosti)

    matrika = np.array(matrika)
    w = np.array(w)
    pop = w
    for _ in range(1, n+1):
        strategija = np.array(s(pop, matrika, nat))
        pop = np.array(pop)
        konstanta = konst_del(strategija, pop, matrika)
        pop = konstanta * (strategija-pop) + pop
    print('x( t={} ) = {}\nx( t={} ) = {}'.format(0, w, n, pop))
    return [w, pop]


def simulacija(st_iteracij=10, nat=1, st_komponent=3, t_max=100):
    for _ in range(st_iteracij):
        vsota1 = 0
        koordinate1 = [0 for _ in range(st_komponent)]
        while vsota1 == 0:
            koordinate1 = [random.randint(0, 10**nat + 1) for _ in range(st_komponent)]
            vsota1 = sum(koordinate1)
        for p in range(len(koordinate1)):
            koordinate1[p] *= 1/vsota1
        iteracija(koordinate1, n=t_max, nat=nat)


vklop = True
while vklop:
    it = input('Stevilo zacetnih x-ov (privzeto: 1): ')
    if it == '':
        it = 1
    st = input('Stevilo komponent x-a (privzeto: 3): ')
    if st == '':
        st = 3
    cas = input('Stevilo iteracij (maksimalen cas, privzeto: 100): ')
    if cas == '':
        cas = 100
    print(' ')
    simulacija(int(it), 1, int(st), int(cas))
    nadaljuj = input("\nNadaljuj ([1]='DA' (privzeto) ali [0]='NE')? ")
    if nadaljuj in {'0'}:
        vklop = False
