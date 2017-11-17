# Dinamika okuzb in imunizacije

import numpy as np
import random

w = w = [0.1, 0.8, 0.1, 0.4, 0.1, 0.9]
natancnost = 1

def Delta():
    koordinate = [random.randint(0,10**natancnost + 1) for i in range(len(w))]
    vsota = sum(koordinate)
    if vsota != 0:
        for k in range(len(koordinate)):
            koordinate[k] *= 1/vsota
    else:
        return [0,0,0]
    return koordinate
# Delta je simpleks (sum_{i=1:n}x_i=1, x_i>=0 za i=1:n)

A = [[0 for i in range(len(w))] for j in range(len(w))]
for i in range(len(w)):
    for j in range(len(w)):
        A[i][j] = (abs(w[i] - w[j]))**(1/2)
# hitrost konvergence in limita odvisna od definicije a_{i,j}

def Y(x, A = A):
    x = np.array(x)
    A = np.array(A)
    Gamma = []
    while len(Gamma) == 0:
        y = Delta()
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

pop = w
for t in range(300):
    s = np.array(S(pop))
    pop = np.array(pop)
    pop += delta(s,pop) * (s-pop)
    print(pop)
