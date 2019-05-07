import numpy as np
import random
import matplotlib.pyplot as plt

#ZDEFINIOWANIE POTRZEBNYCH DANYCH

realizatory = np.array([1, 2], dtype = int)
zadania = np.array([1, 2, 3, 4, 5, 6], dtype = int)

czas_zadania_r_1 = np.random.randint(100, size = len(zadania) - 1)
czas_zadania_r_2 = np.random.randint(100, size = len(zadania) - 1)

czas_dojazdu_r_1 = np.random.randint(100, size = (len(zadania), len(zadania)))
czas_dojazdu_r_2 = np.random.randint(100, size = (len(zadania), len(zadania)))
np.fill_diagonal(czas_dojazdu_r_1, 200)
np.fill_diagonal(czas_dojazdu_r_2, 200)

czas_dojazdu_r_1_t = czas_dojazdu_r_1.transpose()
czas_dojazdu_r_2_t = czas_dojazdu_r_2.transpose()
czas_r_1_max = []
czas_r_2_max = []
czas_r_1_min = []
czas_r_2_min = []

# print(czas_zadania_r_1)
# print(czas_dojazdu_r_1_t)

#czasy_maxymalne dla danego realizatroa i danego zadania
# for i in range(len(czas_zadania_r_1)):
#     maxi = None
#     suma = None
#     pom = czas_zadania_r_1[i]
#     for j in range(len(czas_dojazdu_r_1)):
#         maxi = max(czas_dojazdu_r_1_t[i])
#     suma = pom + maxi
#     czas_r_1_max.append(suma)
#
# for i in range(len(czas_zadania_r_2)):
#     maxi = None
#     suma = None
#     pom = czas_zadania_r_1[i]
#     for j in range(len(czas_dojazdu_r_2)):
#         maxi = max(czas_dojazdu_r_2_t[i])
#     suma = pom + maxi
#     czas_r_2_max.append(suma)
#
# czas_max = np.vstack((czas_r_1_max, czas_r_2_max))
# print(czas_max)

#czasy_minimalne dla danego realizatroa i danego zadania
for i in range(len(czas_zadania_r_1)):
    mini = None
    suma = None
    pom = czas_zadania_r_1[i]
    for j in range(len(czas_dojazdu_r_1)):
        mini = min(czas_dojazdu_r_1_t[i])
    suma = pom + mini
    czas_r_1_min.append(suma)

for i in range(len(czas_zadania_r_2)):
    mini = None
    suma = None
    pom = czas_zadania_r_1[i]
    for j in range(len(czas_dojazdu_r_2)):
        mini = min(czas_dojazdu_r_2_t[i])
    suma = pom + mini
    czas_r_2_min.append(suma)

czas_min = np.vstack((czas_r_1_min, czas_r_2_min))
#print(czas_min)


#Przypadek aproksymacyjnych algorytmow rozwiazywania problemu

#krok1
c = np.zeros((len(realizatory), (len(zadania))), int) #macierz przypisania zadan
q = np.zeros((1,len(realizatory)), int) #macierz pomocnicza do zapamietywania danego czasu zadania

print(q)
#krok2

czas_dojazdu = np.concatenate(([czas_dojazdu_r_1], [czas_dojazdu_r_2]), axis = 0)
#print(czas_dojazdu)

#krok2

pom_czas_zadania_r_1 = czas_zadania_r_1
pom_czas_zadania_r_2 = czas_zadania_r_2
dlugosc = len(czas_zadania_r_1)
pom_dlugosc = 0
suma_r_1 = 0
suma_r_2 = 0

while pom_dlugosc < dlugosc:
    q[0][0] = czas_zadania_r_1[pom_dlugosc]
    q[0][1] = czas_zadania_r_2[pom_dlugosc]
    suma_r_1 = suma_r_1 + q[0][0]
    suma_r_2 = suma_r_2 + q[0][1]
    if suma_r_1 < suma_r_2:
        c[0][pom_dlugosc] = 1
        suma_r_2 = suma_r_2 - q[0][1]
    else:
        c[1][pom_dlugosc] = 1
        suma_r_1 = suma_r_1 - q[0][0]
    pom_dlugosc += 1
#print(c)



U_R_1 = np.array([], dtype = int)
#U_R_1 = np.append(U_R_1, zadania[-1])
U_R_2 = np.array([], dtype = int)
#U_R_2 = np.append(U_R_2, zadania[-1])
U = np.zeros((len(c), len(zadania) - 1), dtype = int)
U_1 = np.zeros((len(c), len(zadania) - 1), dtype = int)
U_2 = np.zeros((len(c), len(zadania) - 1), dtype = int)

for i in range(len(c)):
    for j in range(len(zadania) - 1):
        if c[i][j] == 1:
            U[i][j] = (j+1)
        else:
            U[i][j] = 0
#print(U)

for i in range(len(zadania) - 1):
    if c[0][i] == 1:
        U_R_1 = np.append(U_R_1, U[0][i])
U_R_1 = np.append(U_R_1, zadania[-1])


for i in range(len(zadania) - 1):
    if c[1][i] == 1:
        U_R_2 = np.append(U_R_2, U[1][i])
U_R_2 = np.append(U_R_2, zadania[-1])
#print(c)
#print(U_R_1)
#print(U_R_2)


c[0][-1] = 1
c[1][-1] = 1
print(U_R_1)
print(U_R_2)
U_R_1_final = np.array([], dtype = int)
U_R_2_final = np.array([], dtype = int)
U_R_1_final = np.append(U_R_1_final, zadania[-1])
U_R_2_final = np.append(U_R_2_final, zadania[-1])



while U_R_1.size != 0:
    czasy_poszeregowane_r_1 = np.zeros((len(U_R_1), len(U_R_1)), int)
    for i in range(len(U_R_1)):
        a = U_R_1[i]
        for j in range(len(U_R_1)):
            b = U_R_1[j]
            czasy_poszeregowane_r_1[i][j] = czas_dojazdu_r_1[a-1][b-1]

    dlugosc_czasow_r_1 = int(len(czasy_poszeregowane_r_1) - 1)
    suma_dojazdow_r_1 = np.array([], dtype = int)

    for i in range(len(U_R_1)):
        suma = czasy_poszeregowane_r_1[i][dlugosc_czasow_r_1] + czasy_poszeregowane_r_1[dlugosc_czasow_r_1][i]
        #print(suma)
        suma_dojazdow_r_1 = np.append(suma_dojazdow_r_1, suma)
        # print(czasy_poszeregowane_r_1[i][dlugosc_czasow_r_1])
        # print(czasy_poszeregowane_r_1[dlugosc_czasow_r_1][i])
    minimum_r_1 = min(suma_dojazdow_r_1)
    suma_dojazdow_r_1_final = np.array([], dtype = int)
    suma_dojazdow_r_1_final = np.append(suma_dojazdow_r_1_final, minimum_r_1)
    indx_1 = np.where(suma_dojazdow_r_1 == minimum_r_1)
    U_R_1_final = np.append(U_R_1_final, U_R_1[indx_1])
    U_R_1 = np.delete(U_R_1, indx_1)


while U_R_2.size != 0:
    czasy_poszeregowane_r_2 = np.zeros((len(U_R_2), len(U_R_2)), int)
    for i in range(len(U_R_2)):
        a = U_R_2[i]
        for j in range(len(U_R_2)):
            b = U_R_2[j]
            czasy_poszeregowane_r_2[i][j] = czas_dojazdu_r_2[a - 1][b - 1]
    dlugosc_czasow_r_2 = int(len(czasy_poszeregowane_r_2) - 1)
    suma_dojazdow_r_2 = np.array([], dtype = int)

    for i in range(len(U_R_2)):
        suma = czasy_poszeregowane_r_2[i][dlugosc_czasow_r_2] + czasy_poszeregowane_r_2[dlugosc_czasow_r_2][i]
        suma_dojazdow_r_2 = np.append(suma_dojazdow_r_2, suma)
    minimum_r_2 = min(suma_dojazdow_r_2)
    indx_2 = np.where(suma_dojazdow_r_2 == minimum_r_2)
    suma_dojazdow_r_2_final = np.array([], dtype = int)
    suma_dojazdow_r_2_final = np.append(suma_dojazdow_r_2_final, minimum_r_2)
    U_R_2_final = np.append(U_R_2_final, U_R_2[indx_2])
    U_R_2 = np.delete(U_R_2, indx_2)


xlab1 = []
for i in range(len(U_R_1_final)):
    xlab1.append(i + 1)

xlab2 = []
for i in range(len(U_R_2_final)):
    xlab2.append(i + 1)

ylab1 = []
for i in U_R_1_final:
    if i == 6:
        ylab1.append('baza')
    else:
        ylab1.append('zad_' + str(i))


ylab2 = []
for i in U_R_2_final:
    if i == 6:
        ylab2.append('baza')
    else:
        ylab2.append('zad_' + str(i))




# plt.figure(1)
# plt.subplot(221).title.set_text('Realizator 1')
# plt.scatter(xlab1, ylab1)
# plt.xlim(1, 6)
# plt.xlabel("Kolejnosc zadania")
#
# plt.subplot(224).title.set_text('Realizator 2')
# plt.scatter(xlab2, ylab2)
# plt.xlim(1, 6)
# plt.xlabel("Kolejnosc zadania")
# plt.show()
# print(U_R_1_final)
# print(U_R_2_final)
print(len(czas_zadania_r_1))