import numpy as np
import random

global srednia_sys, srednia_sek

srednia_sys = 0

srednia_sek = 0

licz_zadan = 5


for j in range(0, 10):

    licz_realizatorow = 2


    realizatory = np.array([], dtype=int)

    zadania = np.array([], dtype=int)

    # WYPELNIENIE MACIERZY POTRZEBNYMI DANYMI

    for i in range(licz_realizatorow):
        realizatory = np.append(realizatory, i + 1)

    for i in range(licz_zadan):
        zadania = np.append(zadania, i + 1)

    #czasy_zadan = np.array([[57, 64, 60, 54, 56],
    #                      [62, 52, 53, 59, 58]])

    czasy_zadan = np.random.randint(50, 70, size=((len(realizatory), len(zadania))))


    czasy_zadan_t = czasy_zadan.transpose()


    czasy_dojazdu = np.random.randint(50, 70, size=(len(realizatory), len(zadania), len(zadania)))

    for i in range(len(realizatory)):
        np.fill_diagonal(czasy_dojazdu[i], 400)


    # czasy_dojazdu = np.array([[[400, 52, 58, 64, 53, 57],
    #                           [57, 400, 55, 53, 61, 59],
    #                           [69, 54, 400, 52, 58, 55],
    #                           [56, 58, 57, 400, 54, 62],
    #                           [51, 63, 61, 53, 400, 65],
    #                           [54, 59, 62, 56, 58, 400]],
    #                          [[400, 55, 62, 58, 57, 60],
    #                           [64, 400, 65, 53, 64, 52],
    #                           [62, 57, 400, 52, 52, 62],
    #                           [52, 58, 61, 400, 55, 63],
    #                           [53, 59, 54, 57, 400, 54],
    #                           [57, 53, 57, 60, 53, 400]]])

    # for i in range(len(realizatory)):
    #     np.fill_diagonal(czasy_dojazdu[i], 1)

    czasy_dojazdu_t = np.zeros((len(realizatory), len(zadania), len(zadania)), dtype = int)


    for i in range(len(realizatory)):
        czasy_dojazdu_t[i] = czasy_dojazdu[i].transpose()

    czasy_mini = np.zeros((len(realizatory), len(zadania) - 1), dtype = int)

    for i in range(len(realizatory)):
        for j in range(len(zadania) - 1):
            for k in range(len(zadania) - 1):
                minimum = min(czasy_dojazdu_t[i][j])
                suma = minimum + czasy_zadan[i][j]
                czasy_mini[i][j] = suma


    c = np.zeros((len(realizatory), len(zadania)), dtype = int) #MACIERZ PRZYPISANIA ZADAN

    suma = np.zeros((len(realizatory), 1), dtype = int)

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
            np.fill_diagonal(czasy_dojazdu[i], 400)

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

                pom_suma = []

                for j in range(dlugosc_listy):
                    gprim = pom_slownik[j]
                    for k in range(dlugosc_slownika - 1):
                        gie = pom_c[k]
                        ha = pom_c[k + 1]
                        suma = czasy_dojazdu[i - 1][gie - 1][gprim - 1] + czasy_dojazdu[i - 1][gprim - 1][ha - 1] - czasy_dojazdu[i - 1][gie - 1][ha - 1]
                        pom_suma.append(suma)
                        check = np.amin(pom_suma)
                        if suma == check:
                            indeks = pom_c.index(ha)
                            nowy = gprim
                pom_c.insert(indeks + 1, nowy)
                c_final[i] = pom_c
                indeks = pom_slownik.index(nowy)
                pom_slownik.pop(indeks)


        return c_final

    jakosc = komiwojazer()


    def quality(decyzja):

        global Q_sys

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

        return Q_sys

    quality(jakosc)


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

    wi = szeregowanie_1()


    def komiwojazer_1():
        for i in range(len(realizatory)):
            np.fill_diagonal(czasy_dojazdu[i], 400)

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

                pom_suma = []

                for j in range(dlugosc_listy):
                    gprim = pom_slownik[j]
                    for k in range(dlugosc_slownika - 1):
                        gie = pom_c[k]
                        ha = pom_c[k + 1]
                        suma = czasy_dojazdu[i - 1][gie - 1][gprim - 1] + czasy_dojazdu[i - 1][gprim - 1][ha - 1] - \
                               czasy_dojazdu[i - 1][gie - 1][ha - 1]
                        pom_suma.append(suma)
                        check = np.amin(pom_suma)
                        if suma == check:
                            indeks = pom_c.index(ha)
                            nowy = gprim
                pom_c.insert(indeks + 1, nowy)
                c_final[i] = pom_c
                indeks = pom_slownik.index(nowy)
                pom_slownik.pop(indeks)

        return c_final


    jakosc_1 = komiwojazer_1()


    def quality_1(decyzja_1):

        global Q_sek

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

        return Q_sek


    quality_1(jakosc_1)

    srednia_sys = srednia_sys + Q_sys

    srednia_sek = srednia_sek + Q_sek

# srednia_sys = srednia_sys/10
#
# srednia_sek - srednia_sek/10

delta = (srednia_sek - srednia_sys)/srednia_sys
delta = delta * 100

print(delta)
