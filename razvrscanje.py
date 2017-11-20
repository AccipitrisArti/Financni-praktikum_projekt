# Dinamika okuzb in imunizacije

import numpy as np     # knjiznica za numericno ucinkovito racunanje
import random


# privzete vrednosti (stevilo zacetkov, stevilo komponent, maksimalen cas)
it1, st1, cas1 = 5, 4, 200


def delta(w, nat):     # simpleks {x; sum_{i=1:n}x_i=1, x_i>=0 za i=1:n}
    vsota = 0
    koordinate = [0 for _ in range(len(w))]
    while vsota == 0:
        koordinate = [random.randint(0, 10**nat + 1) for _ in range(len(w))]
        vsota = sum(koordinate)
    for k in range(len(koordinate)):
        koordinate[k] *= 1/vsota
    return np.array(koordinate)


def gamma(x, matrika, nat):   # iskanje elementa y\in\Delta, ki zadosca pogoju (y-x)^T*A*x > 0
    x = np.array(x)
    matrika = np.array(matrika)
    for _ in range(10000):
        y = np.array(delta(x, nat))
        if len(x) == len(y):
            z = np.array([y[i]-x[i] for i in range(len(x))])
            if np.dot(np.dot(z, matrika), x) > 0:
                return y
    return None


def s(x, matrika, nat):     # izbira strategije y
    y = gamma(x, matrika, nat)
    if y is None:
        return x
    return y


def konst_del(y, x, matrika):     # izracun konstante \delta_y(x)
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


def iteracija(x, n, nat):    # izracun strategije ob casu n, ob konstantni matriki koristnosti
    w = [x[i] / sum(x) for i in range(len(x))]

    matrika = [[0 for _ in range(len(w))] for _ in range(len(w))]
    for i in range(len(w)):
        for j in range(len(w)):
            matrika[i][j] = abs(w[i] - w[j])
    # hitrost konvergence in limita odvisna od definicije matrike A_{i,j}
    # A je matrika izplacil (koristnosti) generirana kot A_{i,j} = abs(x_i(0) - x_j(0))

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


# =========================(odstrani)
def iteracija2(x, n, nat):    # izracun strategije ob casu n, ob matriki koristnosti odvisni od casa
    w = [x[i] / sum(x) for i in range(len(x))]
    w = np.array(w)
    pop = w
    for _ in range(1, n+1):
        matrika = [[0 for _ in range(len(pop))] for _ in range(len(pop))]
        for i in range(len(pop)):
            for j in range(len(pop)):
                matrika[i][j] = abs(pop[i] - pop[j])
        # hitrost konvergence in limita odvisna od definicije matrike A_{i,j}
        # A je matrika izplacil (koristnosti) generirana kot A_{i,j} = abs(x_i(t) - x_j(t))
        matrika = np.array(matrika)
        strategija = np.array(s(pop, matrika, nat))
        pop = np.array(pop)
        konstanta = konst_del(strategija, pop, matrika)
        pop = konstanta * (strategija-pop) + pop
    print('x( t={} ) = {}\nx( t={} ) = {}'.format(0, w, n, pop))
    return [w, pop]
# =========================


# =========================(spremeni)
def simulacija(st_iteracij=10, nat=1, st_komponent=3, t_max=100, ite=0):
    # =========================
    #   iteracija nakljucno generiranih zacetnih strategij
    for _ in range(st_iteracij):
        vsota1 = 0
        koordinate1 = [0 for _ in range(st_komponent)]
        while vsota1 == 0:
            koordinate1 = [random.randint(0, 10**nat + 1) for _ in range(st_komponent)]
            vsota1 = sum(koordinate1)
        for p in range(len(koordinate1)):
            koordinate1[p] *= 1/vsota1
        # =========================(spremeni)
        if ite == 0:
            iteracija(koordinate1, n=t_max, nat=nat)
        else:
            iteracija2(koordinate1, n=t_max, nat=nat)
        # =========================


#    uporabniku prijazen program
vklop = True
while vklop:
    it = input('Stevilo zacetnih x-ov (privzeto: {}): '.format(it1))
    if it == '':
        it = it1
    st = input('Stevilo komponent x-a (privzeto: {}): '.format(st1))
    if st == '':
        st = st1
    cas = input('Stevilo iteracij (maksimalen cas, privzeto: {}): '.format(cas1))
    if cas == '':
        cas = cas1
    # =========================(odstrani)
    itr = input('Nacin iteracije ([1] = A odvisen od t, [(drugo)] = A konstanten (privzeto))\n'
                '[torej A_{i,j} = abs(x_i - x_j) v odvisnosti od casa ali ne]: ')
    if itr != '1':
        itr = 0
    # =========================
    # =========================(spremeni)
    print('\nSimulacija(st_zacetkov = {}, st_akcij = {}, Max_cas = {}, nacin_iteracije = {})\n'.format(
        it, st, cas, itr
    ))
    simulacija(int(it), 1, int(st), int(cas), itr)
    # =========================
    nadaljuj = input("\nNadaljuj ([1]='DA' (privzeto) ali [0]='NE')? ")
    if nadaljuj in {'0'}:
        vklop = False
