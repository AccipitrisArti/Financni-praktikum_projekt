import numpy as np

x = [1,2]
natancnost = 1
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

A = [[0 for i in range(len(x))] for j in range(len(x))]
for i in range(len(x)):
    for j in range(len(x)):
        A[i][j] = abs(x[i] - x[j])

def Y(x, A = A, Delta = Delta):
    x = np.array(x)
    A = np.array(A)
    Gamma = []
    for y in Delta:
        y = np.array(y)
        if sum(sum(np.transpose((y - x) * A) * (y - x))) > 0:
           Gamma.append(y)
    return Gamma

def S(x):
    y = Y(x)
    if len(y) != 0:
        return y[0]
    return x

def delta(y,x,A=A):
    x = np.array(x)
    y = np.array(y)
    A = np.array(A)
    mx = sum(sum((y - x) * A * np.transpose([x])))
    my = sum(sum(np.transpose((y - x) * A) * y))
    if my-mx < 0:
        return min(-mx/(my-mx),1)
    return 1

pop = x
for t in range(10):
    s = np.array(S(pop))
    pop = np.array(pop)
    pop = delta(s,pop) * (s-pop) + pop
    print(pop)