import numpy as np
import random
import pandas as pd


def menu_prime():
    print(30 * '-' , 'MENU' , 30 * '-')
    print('1. Szeregowanie zadan')
    print('2. Wyjscie')
    print(66 * '-')

def menu():
    print(28 * '-' , 'KRYTERIA' , 28 * '-')
    print('1. Czasy MAX')
    print('2. Czasy MIN')
    print(66 * '-')

petla = True

while petla:

    menu_prime()

    wejscie = input('Podaj [1 lub 2]: ')

    if wejscie == '1':

        licz_realizatorow = int(input('Podaj liczbe realizatorow(1-15): '))
        licz_zadan = int(input('Podaj liczbe zadan(1-100, uwzgledniajac baze w postaci ostatniego zadania): '))
        realizatory = np.array([], dtype=int)
        zadania = np.array([], dtype=int)

        # WYPELNIENIE MACIERZY POTRZEBNYMI DANYMI

        for i in range(licz_realizatorow):
            realizatory = np.append(realizatory, i + 1)

        for i in range(licz_zadan):
            zadania = np.append(zadania, i + 1)

        czasy_zadan = np.random.randint(20, 120, size=((len(realizatory), len(zadania))))
        czasy_zadan_t = czasy_zadan.transpose()

        czasy_dojazdu = np.random.randint(10, 40, size=(len(realizatory), len(zadania), len(zadania)))
        czasy_dojazdu_t = np.zeros((len(realizatory), len(zadania), len(zadania)), dtype=int)

        for i in range(len(realizatory)):
            czasy_dojazdu_t[i] = czasy_dojazdu[i].transpose()


        menu()

        wybor = input('Podaj [1 lub 2]: ')


        if wybor == '1':

            def systemowe():
                #MAKSYMALIZUJEMY CZAS DOJAZDU

                for i in range(len(realizatory)):
                    np.fill_diagonal(czasy_dojazdu[i], 1)

                czasy_maxi = np.zeros((len(realizatory), len(zadania) - 1), dtype=int)

                for i in range(len(realizatory)):
                    for j in range(len(zadania) - 1):
                        for k in range(len(zadania) - 1):
                            maximum = max(czasy_dojazdu_t[i][j])
                            suma = maximum + czasy_zadan[i][j]
                            czasy_maxi[i][j] = suma

                c = np.zeros((len(realizatory), len(zadania)), dtype=int)  # MACIERZ PRZYPISANIA ZADAN
                suma = np.zeros((len(realizatory), 1), dtype=int)

                def szeregowanie():

                    for i in range(len(zadania) - 1):
                        for j in range(len(realizatory)):
                            suma[j] = suma[j] + czasy_maxi[j][i]
                        maximum = np.amax(suma)
                        for k in range(len(realizatory)):
                            if suma[k] != maximum:
                                suma[k] = suma[k] - czasy_maxi[k][i]
                            elif suma[k] == maximum:
                                c[k][i] = 1
                                maximum = 0

                    for i in range(len(realizatory)):
                        for j in range(len(zadania) - 1):
                            if c[i][j] == 1:
                                c[i][j] = j + 1
                                c[i][-1] = zadania[-1]
                    # print(c)
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
                                    suma_1 = czasy_dojazdu[i - 1][gie - 1][gprim - 1] + czasy_dojazdu[i - 1][gprim - 1][
                                        ha - 1] - czasy_dojazdu[i - 1][gie - 1][ha - 1]
                                    suma_2 = czasy_dojazdu[i - 1][gprim - 1][idx2 - 1]
                                    if suma_1 < suma_2:
                                        pom_c.insert(pom_c.index(ha), gprim)
                                        c_final[i] = pom_c
                            pom_lista.append(pom_slownik.pop(indx))
                            pom_lista = []
                    return c_final

                jakosc = komiwojazer()

                def quality(decyzja):

                    Qual = []

                    for i in range(1, len(decyzja) + 1):
                        pom_czasy_zadan = czasy_zadan[i - 1].tolist()
                        pom_czasy_zadan.append(0)
                        jakosc = 0
                        dojazdy = 0
                        pom_lista = decyzja[i]
                        for j in range(len(pom_lista) - 1):
                            indx1 = pom_lista[j]
                            indx2 = pom_lista[j + 1]
                            dojazdy = dojazdy + czasy_dojazdu[i - 1][indx1 - 1][indx2 - 1]
                        for k in decyzja[i]:
                            jakosc = jakosc + pom_czasy_zadan[k - 1]
                        jakosc = jakosc + dojazdy
                        Qual.append(jakosc)

                    Q_sys = max(Qual)
                    return Q_sys

                quality(jakosc)

            def sekwencyjne():

                c = np.zeros((len(realizatory), len(zadania)), dtype=int)  # MACIERZ PRZYPISANIA ZADAN

                suma = np.zeros((len(realizatory), 1), dtype=int)

                def szeregowanie():

                    for i in range(len(zadania) - 1):
                        for j in range(len(realizatory)):
                            suma[j] = suma[j] + czasy_zadan_t[i][j]
                        maximum = np.amax(suma)
                        indx = np.argmax(suma)
                        for k in range(len(realizatory)):
                            if suma[k] != maximum:
                                c[indx][i] = 1
                                suma[k] -= czasy_zadan_t[i][k]

                    for i in range(len(realizatory)):
                        for j in range(len(zadania) - 1):
                            if c[i][j] == 1:
                                c[i][j] = j + 1
                                c[i][-1] = zadania[-1]

                    #print(c)
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
                                    suma_1 = czasy_dojazdu[i - 1][gie - 1][gprim - 1] + czasy_dojazdu[i - 1][gprim - 1][
                                        ha - 1] - czasy_dojazdu[i - 1][gie - 1][ha - 1]
                                    suma_2 = czasy_dojazdu[i - 1][gprim - 1][idx2 - 1]
                                    if suma_1 < suma_2:
                                        pom_c.insert(pom_c.index(ha), gprim)
                                        c_final[i] = pom_c
                            pom_lista.append(pom_slownik.pop(indx))
                            pom_lista = []
                    return c_final

                jakosc = komiwojazer()

                def quality(decyzja):

                    Qual = []

                    for i in range(1, len(decyzja) + 1):
                        pom_czasy_zadan = czasy_zadan[i - 1].tolist()
                        pom_czasy_zadan.append(0)
                        jakosc = 0
                        dojazdy = 0
                        pom_lista = decyzja[i]
                        for j in range(len(pom_lista) - 1):
                            indx1 = pom_lista[j]
                            indx2 = pom_lista[j + 1]
                            dojazdy = dojazdy + czasy_dojazdu[i - 1][indx1 - 1][indx2 - 1]
                        for k in decyzja[i]:
                            jakosc = jakosc + pom_czasy_zadan[k - 1]
                        jakosc = jakosc + dojazdy
                        Qual.append(jakosc)

                    Q_sek = max(Qual)
                    return Q_sek

                quality(jakosc)

            systemowe()
            sekwencyjne()

        elif wybor == '2':

            def systemowe():

                #MINIMALIZUJEMY CZAS DOJAZDU

                np.fill_diagonal(czasy_dojazdu, 200)

                czasy_mini = np.zeros((len(realizatory), len(zadania)), dtype=int)

                for i in range(len(realizatory)):
                    for j in range(len(zadania)):
                        minimum = None
                        suma = None
                        pom = czasy_zadan[i][j]
                        for k in range(len(zadania)):
                            minimum = min(czasy_dojazdu_t[k])
                            suma = pom + minimum
                            czasy_mini[i][j] = suma

                c = np.zeros((len(realizatory), len(zadania)), dtype=int)  # MACIERZ PRZYPISANIA ZADAN
                pom_czasy_zadan = czasy_zadan.transpose()
                suma = np.zeros((len(realizatory), 1), dtype=int)

                def szeregowanie():

                    for i in range(len(zadania)):
                        for j in range(len(realizatory)):
                            pomoc = pom_czasy_zadan[i][j]
                            suma[j] = suma[j] + pomoc + czasy_mini[j][i]
                        mini = np.amin(suma)
                        indx = np.argmin(suma)
                        for k in range(len(realizatory)):
                            if suma[k] != mini:
                                c[indx][i] = 1
                                suma[k] = suma[k] - pom_czasy_zadan[i][k] - czasy_mini[k][i]
                    for i in range(len(realizatory)):
                        c[i][-1] = 1

                    for i in range(len(realizatory)):
                        for j in range(len(zadania)):
                            if c[i][j] == 1:
                                c[i][j] = j + 1
                                c[i][-1] = zadania[-1]

                    print(c)
                    return c

                x = szeregowanie()


                def komiwojazer():

                    np.fill_diagonal(czasy_dojazdu, 200)
                    slownik = {}
                    dlugosc_calosci = 0
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

                        while pom_slownik:
                            dlugosc_listy = len(pom_slownik)
                            pom_czasy = []
                            for j in range(dlugosc_listy):
                                idx1 = pom_slownik[j]
                                idx2 = pom_slownik[-1]
                                suma = czasy_dojazdu[idx1 - 1][idx2 - 1] + czasy_dojazdu[idx2 - 1][idx1 - 1]
                                pom_czasy.append(suma)
                            mini = min(pom_czasy)
                            indx = pom_czasy.index(mini)
                            pom_lista.append(pom_slownik.pop(indx))
                            c_final[i] = np.append(c_final[i], pom_lista)
                            pom_lista = []

                    print(c_final)
                    return c_final

                jakosc = komiwojazer()


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
                    Q_sys = max(Qual)
                    print(Q_sys)
                    return Q_sys

                quality(jakosc)

            def sekwencyjne():

                c = np.zeros((len(realizatory), len(zadania)), dtype=int)  # MACIERZ PRZYPISANIA ZADAN

                suma = np.zeros((len(realizatory), 1), dtype=int)

                def szeregowanie():

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
                    print(c)
                    return c

                szeregowanie()

                def komiwojazer():

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
                        pom_slownik = slownik[i].tolist()

                        while pom_slownik:
                            dlugosc_listy = len(pom_slownik)
                            pom_czasy = []
                            for j in range(dlugosc_listy):
                                idx1 = pom_slownik[j]
                                idx2 = pom_slownik[-1]
                                suma = czasy_dojazdu[idx1 - 1][idx2 - 1] + czasy_dojazdu[idx2 - 1][idx1 - 1]
                                pom_czasy.append(suma)
                            mini = min(pom_czasy)
                            indx = pom_czasy.index(mini)
                            pom_lista.append(pom_slownik.pop(indx))
                            c_final[i] = np.append(c_final[i], pom_lista)
                            pom_lista = []

                    print(c_final)
                    return c_final


                jakosc = komiwojazer()

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
                    print(Q_sek)
                    return Q_sek

                quality(jakosc)

            systemowe()
            sekwencyjne()

    elif wejscie == '2':
        petla = False
