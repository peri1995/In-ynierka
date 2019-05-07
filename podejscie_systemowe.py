import numpy as np
import random
import pandas as pd


def menu():
    print(30 * '-' , 'MENU' , 30 * '-')
    print('1. Czasy MAX')
    print('2. Czasy MIN')
    print('3. Wyjscie')
    print(66 * '-')

petla = True

while petla:

    licz_realizatorow = int(input('Podaj liczbe realizatorow(1-15): '))
    licz_zadan = int(input('Podaj liczbe zadan(1-100): '))
    realizatory = np.array([], dtype=int)
    zadania = np.array([], dtype=int)

    menu()

    wybor = input('Podaj [1-3]: ')



    if wybor == '1':

        #MAKSYMALIZUJEMY CZAS DOJAZDU + WYKONANIA ZADANIA

        # WYPELNIENIE MACIERZY POTRZEBNYMI DANYMI

        for i in range(licz_realizatorow):
            realizatory = np.append(realizatory, i + 1)

        for i in range(licz_zadan):
            zadania = np.append(zadania, i + 1)

        czasy_zadan = np.random.randint(30, 180, size=((len(realizatory), len(zadania))))

        czasy_dojazdu = np.random.randint(15, 30, size=(len(zadania), len(zadania)))
        np.fill_diagonal(czasy_dojazdu, 1)

        czasy_dojazdu_t = czasy_dojazdu.transpose()

        czasy_maxi = np.zeros((len(realizatory), len(zadania)), dtype=int)

        for i in range(len(realizatory)):
            for j in range(len(zadania)):
                maxi = None
                suma = None
                pom = czasy_zadan[i][j]
                for k in range(len(zadania)):
                    maxi = max(czasy_dojazdu_t[k])
                    suma = pom + maxi
                    czasy_maxi[i][j] = suma

        print(czasy_maxi)
        c = np.zeros((len(realizatory), len(zadania)), dtype=int)  # MACIERZ PRZYPISANIA ZADAN
        q = np.zeros((len(realizatory), 1), dtype=int)  # MACIERZ POMOCNICZA
        dlugosc = len(zadania)
        pom_czasy_zadan = czasy_zadan.transpose()
        suma = np.zeros((len(realizatory), 1), dtype=int)

        def szeregowanie(czas):

            for i in range(len(zadania)):
                for j in range(len(realizatory)):
                    pomoc = pom_czasy_zadan[i][j]
                    suma[j] = suma[j] + pomoc + czasy_maxi[j][i]
                mini = np.amin(suma)
                indx = np.argmin(suma)
                for k in range(len(realizatory)):
                    if suma[k] != mini:
                        c[indx][i] = 1
                        suma[k] = suma[k] - pom_czasy_zadan[i][k] - czasy_maxi[k][i]
            for i in range(len(realizatory)):
                c[i][-1] = 1

            for i in range(len(realizatory)):
                for j in range(len(zadania)):
                    if c[i][j] == 1:
                        c[i][j] = j + 1
                        c[i][-1] = zadania[-1]

        szeregowanie(czasy_maxi)


        def komiwojazer(c):

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

        komiwojazer(c)

    elif wybor == '2':

        #MINIMALIZUJEMY CZAS DOJAZDU + WYKONANIA ZADANIA

        #WYPELNIENIE MACIERZY POTRZEBNYMI DANYMI

        for i in range(licz_realizatorow):
            realizatory = np.append(realizatory, i + 1)

        for i in range(licz_zadan):
            zadania = np.append(zadania, i + 1)

        czasy_zadan = np.random.randint(30, 180, size = ((len(realizatory), len(zadania))))

        czasy_dojazdu = np.random.randint(15, 30, size = (len(zadania), len(zadania)))
        np.fill_diagonal(czasy_dojazdu, 200)

        czasy_dojazdu_t = czasy_dojazdu.transpose()

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

        print(czasy_mini)
        c = np.zeros((len(realizatory), len(zadania)), dtype=int)  # MACIERZ PRZYPISANIA ZADAN
        q = np.zeros((len(realizatory), 1), dtype=int)  # MACIERZ POMOCNICZA
        dlugosc = len(zadania)
        pom_czasy_zadan = czasy_zadan.transpose()
        suma = np.zeros((len(realizatory), 1), dtype=int)

        def szeregowanie(czas):

            for i in range(len(zadania)):
                for j in range(len(realizatory)):
                    pomoc = pom_czasy_zadan[i][j]
                    suma[j] = suma[j] + pomoc
                mini = np.amin(suma)
                indx = np.argmin(suma)
                for k in range(len(realizatory)):
                    if suma[k] != mini:
                        c[indx][i] = 1
                        suma[k] -= pom_czasy_zadan[i][k]
            for i in range(len(realizatory)):
                c[i][-1] = 1

            for i in range(len(realizatory)):
                for j in range(len(zadania)):
                    if c[i][j] == 1:
                        c[i][j] = j + 1
                        c[i][-1] = zadania[-1]

        szeregowanie(czasy_mini)


        def komiwojazer(c):

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

        komiwojazer(c)


    elif wybor == '3':
        petla = False