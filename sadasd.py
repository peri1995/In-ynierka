import numpy as np
import random
import pandas as pd


def dane():

    global licz_realizatorow, licz_zadan, realizatory, zadania, czasy_zadan, czasy_zadan_t, czasy_dojazdu, czasy_dojazdu_t

    licz_realizatorow = int(input('Podaj liczbe realizatorow(1-15): '))
    licz_zadan = int(input('Podaj liczbe zadan(1-100, uwzgledniajac baze w postaci ostatniego zadania): '))
    realizatory = np.array([], dtype=int)
    zadania = np.array([], dtype=int)

    # WYPELNIENIE MACIERZY POTRZEBNYMI DANYMI

    for i in range(licz_realizatorow):
        realizatory = np.append(realizatory, i + 1)

    for i in range(licz_zadan - 1):
        zadania = np.append(zadania, i + 1)

    czasy_zadan = np.random.randint(50, 70, size=((len(realizatory), len(zadania))))
    czasy_zadan_t = czasy_zadan.transpose()

    czasy_dojazdu = np.random.randint(40, 70, size=(len(realizatory), len(zadania), len(zadania)))
    czasy_dojazdu_t = np.zeros((len(realizatory), len(zadania), len(zadania)), dtype=int)

    for i in range(len(realizatory)):
        czasy_dojazdu_t[i] = czasy_dojazdu[i].transpose()

dane()

def systemowe():

    czasy_mini = np.zeros((len(realizatory), len(zadania) - 1), dtype=int)

    for i in range(len(realizatory)):
        for j in range(len(zadania) - 1):
            for k in range(len(zadania) - 1):
                minimum = min(czasy_dojazdu_t[i][j])
                suma = minimum + czasy_zadan[i][j]
                czasy_mini[i][j] = suma

    c = np.zeros((len(realizatory), len(zadania)), dtype=int)  # MACIERZ PRZYPISANIA ZADAN
    suma = np.zeros((len(realizatory), 1), dtype=int)

    def szeregowanie():

        for i in range(len(zadania) - 1):
            for j in range(len(realizatory)):
                suma[j] = suma[j] + czasy_mini[j][i]
            minimum = np.amin(suma)
            for k in range(len(realizatory)):
                if suma[k] != minimum:
                    suma[k] = suma[k] - czasy_mini[k][i]
                elif suma[k] == minimum:
                    c[k][i] = 1
                    minimum = 0

        for i in range(len(realizatory)):
            for j in range(len(zadania) - 1):
                if c[i][j] == 1:
                    c[i][j] = j + 1
                    c[i][-1] = zadania[-1]
        return c

    x = szeregowanie()

    def komiwojazer():

        for i in range(len(realizatory)):
            np.fill_diagonal(czasy_dojazdu[i], 200)

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
            pom_slownik = slownik[i].tolist()
            dlugosc_listy = len(pom_slownik)
            pom_czasy = []
            for j in range(dlugosc_listy):
                idx1 = pom_slownik[j]
                idx2 = pom_slownik[-1]
                suma = czasy_dojazdu[i - 1][idx1 - 1][idx2 - 1] + czasy_dojazdu[i - 1][idx2 - 1][idx1 - 1]
                pom_czasy.append(suma)
            mini = min(pom_czasy)
            indx = pom_czasy.index(mini)
            pom_lista.append(pom_slownik.pop(indx))
            c_final[i] = np.append(c_final[i], pom_lista)
            pom_lista = []
            pom_lista.append(pom_slownik.pop(-1))
            c_final[i] = np.append(c_final[i], pom_lista)
            pom_lista = []
            pom_c = c_final[i].tolist()
            while pom_slownik:
                dlugosc_listy = len(pom_slownik)
                dlugosc_slownika = len(c_final[i])
                for k in range(dlugosc_slownika - 1):
                    gie = pom_c[k]
                    ha = pom_c[k + 1]
                    for j in range(dlugosc_listy):
                        gprim = pom_slownik[j]
                        suma_1 = czasy_dojazdu[i - 1][gie - 1][gprim - 1] + czasy_dojazdu[i - 1][gprim - 1][ha - 1] - \
                                 czasy_dojazdu[i - 1][gie - 1][ha - 1]
                        suma_2 = czasy_dojazdu[i - 1][gprim - 1][idx2 - 1]

                        if suma_1 < suma_2:
                            pom_c.insert(pom_c.index(ha), gprim)
                            c_final[i] = pom_c


                pom_slownik.pop(0)


        return c_final

    jakosc = komiwojazer()

    def quality(decyzja):

        Qual = []

        for i in range(1, len(realizatory) + 1):
            pomka = czasy_zadan[i - 1].tolist()
            pomka.append(0)
            sumka = 0
            for j in range(len(decyzja[i]) - 1):
                gie = decyzja[i][j]
                ha = decyzja[i][j + 1]
                sumka = sumka + czasy_dojazdu[i - 1][gie - 1][ha - 1] + pomka[ha - 1]
            Qual.append(sumka)

        Q_sys = max(Qual)

        print(Q_sys)
        return Q_sys

    quality(jakosc)


def sekwencyjne():

    c = np.zeros((len(realizatory), len(zadania)), dtype=int)  # MACIERZ PRZYPISANIA ZADAN
    suma = np.zeros((len(realizatory), 1), dtype=int)

    def szeregowanie_1():

        for i in range(len(zadania) - 1):
            for j in range(len(realizatory)):
                suma[j] = suma[j] + czasy_zadan[j][i]
            minimum = np.amin(suma)
            for k in range(len(realizatory)):
                if suma[k] != minimum:
                    suma[k] = suma[k] - czasy_zadan[k][i]
                elif suma[k] == minimum:
                    c[k][i] = 1
                    minimum = 0

        for i in range(len(realizatory)):
            for j in range(len(zadania) - 1):
                if c[i][j] == 1:
                    c[i][j] = j + 1
                    c[i][-1] = zadania[-1]

        return c

    x_1 = szeregowanie_1()

    def komiwojazer_1():
        for i in range(len(realizatory)):
            np.fill_diagonal(czasy_dojazdu[i], 200)

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
            pom_slownik = slownik[i].tolist()
            dlugosc_listy = len(pom_slownik)
            pom_czasy = []
            for j in range(dlugosc_listy):
                idx1 = pom_slownik[j]
                idx2 = pom_slownik[-1]
                suma = czasy_dojazdu[i - 1][idx1 - 1][idx2 - 1] + czasy_dojazdu[i - 1][idx2 - 1][idx1 - 1]
                pom_czasy.append(suma)
            mini = min(pom_czasy)
            indx = pom_czasy.index(mini)
            pom_lista.append(pom_slownik.pop(indx))
            c_final[i] = np.append(c_final[i], pom_lista)
            pom_lista = []
            pom_lista.append(pom_slownik.pop(-1))
            c_final[i] = np.append(c_final[i], pom_lista)
            pom_lista = []
            pom_c = c_final[i].tolist()
            while pom_slownik:
                dlugosc_listy = len(pom_slownik)
                dlugosc_slownika = len(c_final[i])
                for k in range(dlugosc_slownika - 1):
                    gie = pom_c[k]
                    ha = pom_c[k + 1]
                    for j in range(dlugosc_listy):
                        gprim = pom_slownik[j]
                        suma_1 = czasy_dojazdu[i - 1][gie - 1][gprim - 1] + czasy_dojazdu[i - 1][gprim - 1][
                            ha - 1] - czasy_dojazdu[i - 1][gie - 1][ha - 1]
                        suma_2 = czasy_dojazdu[i - 1][gprim - 1][idx2 - 1]
                        if suma_1 < suma_2:
                            pom_c.insert(pom_c.index(ha), gprim)
                            c_final[i] = pom_c
                pom_slownik.pop(0)

        return c_final

    jakosc_1 = komiwojazer_1()

    def quality_1(decyzja_1):
        Qual = []

        for i in range(1, len(realizatory) + 1):
            pomka = czasy_zadan[i - 1].tolist()
            pomka.append(0)
            sumka = 0
            for j in range(len(decyzja_1[i]) - 1):
                gie = decyzja_1[i][j]
                ha = decyzja_1[i][j + 1]
                sumka = sumka + czasy_dojazdu[i - 1][gie - 1][ha - 1] + pomka[ha - 1]
            Qual.append(sumka)

        Q_sek = max(Qual)

        print(Q_sek)
        return Q_sek

    quality_1(jakosc_1)


systemowe()
sekwencyjne()