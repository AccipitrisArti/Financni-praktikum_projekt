# Dinamika okuzb in imunizacije
# Taja Debeljak in Anze Marinko, financna matematika, financni praktikum

import numpy as np  # knjiznica za numericno ucinkovito racunanje
import random
import turtle

# privzete vrednosti (stevilo zacetkov, stevilo komponent, maksimalen cas, natancnost)
it1, st1, cas1, nat1 = 15, 2, 30, 10
barve1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5),
          (1, 0.5, 0), (1, 0, 0.5), (0.5, 1, 0), (0, 1, 0.5), (0.5, 0, 1), (0, 0.5, 1)]
barve0 = [(1-1/(m**2+1), 1/(m+1), 0) for m in range(20)]


def element_simpleksa(dolzina):
    vek = [0 for _ in range(dolzina+1)]
    for j in range(1, dolzina):
        vek[j] = random.uniform(0, 1)
    vek[dolzina] = 1
    vek.sort()
    vek1 = [0 for _ in range(dolzina)]
    for j in range(dolzina):
        vek1[j] = vek[dolzina - j] - vek[dolzina - j - 1]
    return vek1


def delta(w):  # simpleks {x; sum_{i=1:n}x_i=1, x_i>=0 za i=1:n}
    koordinate = element_simpleksa(len(w))
    return np.array(koordinate)


def gamma(x, matrika):  # iskanje elementa y\in\Delta, ki zadosca pogoju (y-x)^T*A*x > 0
    x = np.array(x)
    matrika = np.array(matrika)
    for _ in range(10000):
        y = np.array(delta(x))
        if len(x) == len(y):
            z = np.array([y[i] - x[i] for i in range(len(x))])
            if np.dot(np.dot(z, matrika), x) > 0:
                return y
    return None


def s(x, matrika):  # izbira strategije y
    y = gamma(x, matrika)
    if y is None:
        return x
    return y


def konst_del(y, x, matrika):  # izracun konstante \delta_y(x)
    matrika = np.array(matrika)
    x = np.array(x)
    y = np.array(y)
    z = np.array([y[i] - x[i] for i in range(len(x))])
    mx = np.dot(np.dot(z, matrika), x)
    my = np.dot(np.dot(z, matrika), y)
    if -1e-16 < my - mx:  # abs(my - mx) < 1e-16 and my - mx > 0
        return 1
    konstanta = - mx / (my - mx)
    if konstanta < 1:
        return konstanta
    return 1


def iteracija(w, n, ponovitev=1):  # izracun strategije ob casu n, ob konstantni matriki koristnosti
    matrika = [[0 for _ in range(len(w))] for _ in range(len(w))]
    for i in range(len(w)):
        for j in range(len(w)):
            if w[i] != w[j]:
                razdalja = 0
                for k in range(len(w[i])):
                    razdalja += (w[i][k] - w[j][k]) ** 2
                matrika[i][j] = 1 / (razdalja) ** (1 / 2)
                # A je matrika podobnosti

    matrika = np.array(matrika)
    w = np.array(w)
    pop = element_simpleksa(len(w))
    for _ in range(1, n + 1):
        strategija = np.array(s(pop, matrika))
        pop = np.array(pop)
        konstanta = konst_del(strategija, pop, matrika)
        pop = konstanta * (strategija - pop) + pop
    # if ponovitev == 1:
    print('x( t={} ) = {}\nx( t={} ) = {}'.format(0, w, n, pop))
    return [w, pop]


def narisi(zelva, koordinate1, gruce, barve=barve0):
    maxx = [max([koordinate1[i][j] for j in range(len(koordinate1[i]))]) for i in range(len(koordinate1))]
    minx = [min([koordinate1[i][j] for j in range(len(koordinate1[i]))]) for i in range(len(koordinate1))]
    if max(gruce) <= len(barve):
        barve = barve1
    for k in range(len(koordinate1)):
        #zelva.goto((koordinate1[k][0]-minx[0]) * 500 / (maxx[0]-minx[0]) - 250,
        #           (koordinate1[k][1]-minx[1]) * 500 / (maxx[1]-minx[1]) - 250)
        zelva.goto(koordinate1[k][0] * 500 - 250,
                   koordinate1[k][1] * 500 - 250)
        zelva.pen(pensize=10)
        if gruce[k] > len(barve):
            zelva.pencolor('grey')
        else:
            zelva.pencolor(barve[gruce[k] - 1])
        zelva.pendown()
        #zelva.goto((koordinate1[k][0]-minx[0]) * 500 / (maxx[0]-minx[0]) - 249,
        #           (koordinate1[k][1]-minx[1]) * 500 / (maxx[1]-minx[1]) - 250)
        zelva.goto(koordinate1[k][0] * 500 - 250 + 1,
                   koordinate1[k][1] * 500 - 250)
        zelva.penup()
    zelva.goto(-1000, -1000)


def koordinatni_sistem(zelva):
    zelva.goto(-250, -250)
    zelva.pendown()
    zelva.goto(-250, 250)
    zelva.penup()
    zelva.goto(251, 250)
    zelva.pendown()
    zelva.goto(251, -250)
    zelva.penup()
    zelva.pen(pencolor='grey')
    for i in range(10):
        zelva.goto(-250, - i * 500 / (10 - 1) + 250)
        zelva.pendown()
        zelva.goto(251, - i * 500 / (10 - 1) + 250)
        zelva.penup()
        zelva.goto(- i * 500 / (10 - 1) + 250, -250)
        zelva.pendown()
        zelva.goto(- i * 500 / (10 - 1) + 251, 250)
        zelva.penup()
    zelva.pen(pensize=10)
    for i in range(len(barve0)):
        if i < len(barve1):
            zelva.pencolor(barve1[i])
            zelva.goto(280, - i * 10 + 250)
            zelva.pendown()
            zelva.goto(281, - i * 10 + 250)
            zelva.penup()
        zelva.pencolor(barve0[i])
        zelva.goto(270, - i * 10 + 250)
        zelva.pendown()
        zelva.goto(271, - i * 10 + 250)
        zelva.penup()
    zelva.goto(-1000, -1000)


def simulacija(st_iteracij=10, st_komponent=3, t_max=100, zel1=False, natancnost=nat1):
    #   iteracija nakljucno generiranih zacetnih strategij
    if zel1 and st_komponent <= 2:
        zelva = turtle.Turtle()
        zelva.clear()
        zelva.hideturtle()
        zelva.speed(0)
        zelva.penup()
        koordinatni_sistem(zelva)
    koordinate1 = [[random.uniform(0, 1) for _ in range(st_komponent)] for _ in range(st_iteracij)]

    kor = koordinate1
    gruca = 0
    gruce = [0 for _ in range(len(kor))]
    while len(kor) > 0:
        gruca += 1
        itr = iteracija(kor, n=t_max, ponovitev=gruca)

        komp = 0
        if len(kor) <= 2:
            for i in range(len(koordinate1)):
                if gruce[i] == 0:
                    gruce[i] = gruca
            kor = []
        else:
            for i in range(len(koordinate1)):
                if gruce[i] == 0:
                    if itr[1][komp] > 10 ** (-(20-natancnost)/(4*len(itr[1]))) * max(itr[1]):
                        gruce[i] = gruca
                    komp += 1
                kor = []
                for i in range(len(gruce)):
                    if gruce[i] == 0:
                        kor.append(koordinate1[i])
    print(gruce)
    if zel1 and st_komponent <= 2:
        narisi(zelva, koordinate1, gruce)
        zelva.goto(-1000, -1000)


# uporabniku prijazen program
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
    if str(st) in {'1', '2'}:
        zel = input('\n[0] = NE\n(privzeto) = DA\nNarisi z zelvico: ')
        if zel == '0':
            zel = False
        else:
            zel = True
    else:
        zel = False
    nat = input('Zeljena natancnost razdelitve (privzeto {}): '.format(nat1))
    if nat not in [str(i) for i in range(20)]:
        nat = nat1
    else:
        nat = int(nat)
    print('\nSimulacija(st_tock = {}, st_komponent = {}, max_cas = {}, zelva = {})\n'.format(
        it, st, cas, zel
    ))
    simulacija(int(it), int(st), int(cas), zel, natancnost=nat)
    nadaljuj = input("\nNadaljuj ([1]='DA' (privzeto) ali [0]='NE')? ")
    if nadaljuj in {'0'}:
        vklop = False
