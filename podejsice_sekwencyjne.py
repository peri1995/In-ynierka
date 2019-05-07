import numpy as np
import random
import pandas as pd


licz_realizatorow = int(input('Podaj liczbe realizatorow(1-15): '))
licz_zadan = int(input('Podaj liczbe zadan(1-100): '))
realizatory = np.array([], dtype=int)
zadania = np.array([], dtype=int)


for i in range(licz_realizatorow):
    realizatory = np.append(realizatory, i + 1)

for i in range(licz_zadan):
    zadania = np.append(zadania, i + 1)

czasy_zadan = np.random.randint(30, 180, size=((len(realizatory), len(zadania))))
czasy_zadan_t = czasy_zadan.transpose()

czasy_dojazdu = np.random.randint(15, 30, size=(len(zadania), len(zadania)))

c = np.zeros((len(realizatory), len(zadania)), dtype=int)  # MACIERZ PRZYPISANIA ZADAN
#q = np.zeros((len(realizatory), 1), dtype=int)  # MACIERZ POMOCNICZA
suma = np.zeros((len(realizatory), 1), dtype=int)

def szeregowanie(czas):

    for i in range(len(zadania)):
        for j in range(len(realizatory)):
            suma[j] = suma[j] + czasy_zadan_t[i][j]
        mini = np.amin(suma)
        indx = np.argmin(suma)
        for k in range(len(realizatory)):
            if suma[k] != mini:
                c[indx][i] = 1
                suma[k] -= czasy_zadan_t[i][k]

    for i in range(len(realizatory)):
        c[i][-1] = 1

    for i in range(len(realizatory)):
        for j in range(len(zadania)):
            if c[i][j] == 1:
                c[i][j] = j + 1
                c[i][-1] = zadania[-1]

szeregowanie(czasy_zadan)


def komiwojazer(c):

    np.fill_diagonal(czasy_dojazdu, 200)
    slownik = {}

    for i in range(len(realizatory)):
        slownik[i + 1] = zadania[-1]

    for i in range(len(realizatory)):
        for j in range(len(zadania)):
            if c[i][j] != 0:
                slownik[i + 1] = np.append(slownik[i + 1], c[i][j])

    for i in range(len(realizatory)):
        slownik[i + 1] = slownik[i + 1][1:]

    c_final = {}

    for i in range(len(realizatory)):
        c_final[i + 1] = zadania[-1]

    pom_dlugosc = len(slownik)
    pom_lista = []

    for i in range(1, pom_dlugosc + 1):
        print(slownik[i])
        pom_slownik = slownik[i].tolist()

        while pom_slownik:
            dlugosc_listy = len(pom_slownik)
            pom_czasy = []
            for j in range(dlugosc_listy):
                idx1 = pom_slownik[j]
                idx2 = pom_slownik[-1]
                print(idx1, idx2)
                suma = czasy_dojazdu[idx1 - 1][idx2 - 1] + czasy_dojazdu[idx2 - 1][idx1 - 1]
                pom_czasy.append(suma)
            print(pom_czasy)
            mini = min(pom_czasy)
            indx = pom_czasy.index(mini)
            pom_lista.append(pom_slownik.pop(indx))
            c_final[i] = np.append(c_final[i], pom_lista)
            pom_lista = []

    return c_final

komiwojazer(c)

jakosc = komiwojazer(c)


def quality(decyzja):
    Qual = []
    for i in range(1, len(decyzja) + 1):
        czasy_zadan[i - 1][-1] = 0
        jakosc = 0
        dojazdy = 0
        pom_lista = decyzja[i].tolist()
        for j in range(len(pom_lista) - 1):
            indx1 = pom_lista[j]
            indx2 = pom_lista[j + 1]
            dojazdy = dojazdy + czasy_dojazdu[indx1 - 1][indx2 - 1]
        for k in decyzja[i]:
            jakosc = jakosc + czasy_zadan[i - 1][k - 1]
        jakosc = jakosc + dojazdy
        Qual.append(jakosc)
    Q_sek = max(Qual)
    #return Q_sek
    print(Q_sek)

quality(jakosc)
