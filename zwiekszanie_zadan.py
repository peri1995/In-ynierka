import numpy as np
import random
import pandas as pd


global srednia_sys, srednia_sek

licz_zadan = 0

tabela = pd.DataFrame()

licz_realizatorow = 2

while licz_zadan <= 95:

    licz_zadan += 5


    for j in range(0, 10):


        realizatory = np.array([], dtype = int)

        zadania = np.array([], dtype = int)

        for i in range(licz_realizatorow):
            realizatory = np.append(realizatory, i + 1)

        for i in range(licz_zadan):
            zadania = np.append(zadania, i + 1)

        czasy_zadan = np.random.randint(20, 90, size=((len(realizatory), len(zadania))))


        czasy_zadan_t = czasy_zadan.transpose()


        czasy_dojazdu = np.random.randint(10, 55, size=(len(realizatory), len(zadania), len(zadania)))

        for i in range(len(realizatory)):
            np.fill_diagonal(czasy_dojazdu[i], 400)


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
                                if indeks == 0:
                                    indeks += 1
                    pom_c.insert(indeks, nowy)
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
                                if indeks == 0:
                                    indeks += 1
                    pom_c.insert(indeks, nowy)
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


        # srednia_sys = round(srednia_sys, 2)
        #
        # srednia_sek = round(srednia_sek, 2)

        delta = ((Q_sek - Q_sys) / Q_sys) * 100

        delta = round(delta, 2)

        tabela = tabela.append({'Ilosc realizatorow': licz_realizatorow, 'Ilosc zadan': licz_zadan, 'Q_sys': Q_sys, 'Q_sek': Q_sek, 'Stosunek Q_sys do Q_sek w %': delta}, ignore_index = True)


        tabelka = pd.DataFrame(data = tabela)

        # tabelka_1 = pd.DataFrame(data=tabela).values
        #
        # print(tabelka_1)


tabelka.to_excel('Iteracja po zadaniach.xlsx', index = False)

#rysunek = tabelka.plot.line(x = 'Ilosc zadan', y = '[(Q_sek - Q_sys)/Q_sys] * 100')
