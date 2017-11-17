# Dinamika okuzb in imunizacije

import numpy as np
import random

x = [0.1, 0.5, 0.4]
natancnost = 2
interval_0_1 = [i / 10**natancnost for i in range(10**natancnost + 1)]

Delta = []
for tocka in range(10**natancnost,(10**natancnost + 1)**len(x) + 1):
    vsotakomp = tocka
    koordinate = [0] * len(x)
    for komponenta in range(len(x)):
        koordinate[komponenta] = (vsotakomp%(10**natancnost + 1))/10**natancnost
        vsotakomp = vsotakomp//(10**natancnost + 1)
    if sum(koordinate) == 1:
        Delta.append(koordinate)
# Delta je simpleks (sum_{i=1:n}x_i=1, x_i>=0 za i=1:n)

A = [[0 for i in range(len(x))] for j in range(len(x))]
for i in range(len(x)):
    for j in range(len(x)):
        A[i][j] = (abs(x[i] - x[j]))**(1/2)
# hitrost konvergence in limita odvisna od definicije a_{i,j}

def Y(x, A = A, Delta = Delta):
    x = np.array(x)
    A = np.array(A)
    Gamma = []
    for y in Delta:
        y = np.array(y)
        z = [y[i]-x[i] for i in range(len(x))]
        if np.dot(np.dot(z, A), x) > 0:
           Gamma.append(y)
    return Gamma

def S(x):
    y = Y(x)
    if len(y) != 0:
        return y[random.randint(0,len(Y(x))-1)]
    return x

def delta(y,x,A=A):
    A = np.array(A)
    z = [y[i]-x[i] for i in range(len(x))]
    mx = np.dot(np.dot(z, A), x)
    my = np.dot(np.dot(z, A), y)
    if my-mx < 0:
        return min(-mx/(my-mx),1)
    return 1

pop = x
for t in range(300):
    s = np.array(S(pop))
    pop = np.array(pop)
    pop += delta(s,pop) * (s-pop)
    if t%30 == 0:
        print(pop)
