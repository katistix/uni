def citire_lista():
    sir = input("Introduceti numere separate prin spatiu: ")
    lista = []
    for x in sir.split():
        lista.append(int(x))  # conversie la int
    return lista

# 5
def secventa_egale(lista):
    if not lista: # daca lista e goala
        return []
    
    # presupunem ca cea mai lunga este compusa din primul element
    cea_mai_lunga = [lista[0]]
    curenta = [lista[0]] # secventa potentiala
    for i in range(1, len(lista)): # parcurgem toate elementele listei
        if lista[i] == lista[i-1]: # daca elementele consecutive sunt egale
            curenta.append(lista[i])
        else:
            curenta = [lista[i]]

        # daca secventa curenta este mai lunga, actualizam solutia
        if len(curenta) > len(cea_mai_lunga):
            cea_mai_lunga = curenta[:]
    
    return cea_mai_lunga

# 11
def secventa_suma_maxima(lista):
    # daca lista e goala
    if not lista:
        return []
    
    # initializare variabile
    suma_max = lista[0]
    suma_curenta = lista[0]
    inceput_max = 0
    sfarsit_max = 0
    inceput_curent = 0

    # pentru fiecare element din lista incepand cu al doilea
    for i in range(1, len(lista)):

        # daca luand elementul curent, suma scade, inseamna ca incepem o lista curenta noua
        if suma_curenta + lista[i] < lista[i]:
            suma_curenta = lista[i]
            inceput_curent = i
        else:
            suma_curenta += lista[i]

        # daca am gasit o suma mai mare decat cea maxima de pana atunci, actualizam maximul
        if suma_curenta > suma_max:
            suma_max = suma_curenta
            inceput_max = inceput_curent
            sfarsit_max = i

    # luam un slice din lista initiala, exact cat este cea de suma maxima
    rezultat = lista[inceput_max:sfarsit_max+1]

    return rezultat


# cerinta 12
def semne_contrare(lista):
    if not lista:
        return []

    # initializare variabile
    lungime_maxima = 1
    start_secventa_maxima = 0
    lungime_curenta = 1
    start_curent = 0

    # parcurgem lista incepand cu al doilea element
    for i in range(1, len(lista)):
        # daca semnele se schimba (pozitiv/negativ alternant)
        if (lista[i] > 0 and lista[i-1] < 0) or (lista[i] < 0 and lista[i-1] > 0):
            lungime_curenta += 1
        else:
            # incepem o noua secventa
            start_curent = i
            lungime_curenta = 1

        # actualizam secventa maxima daca cea curenta e mai lunga
        if lungime_curenta > lungime_maxima:
            lungime_maxima = lungime_curenta
            start_secventa_maxima = start_curent

    # luam un slice din lista initiala, exact cat este cea mai lunga secventa
    rezultat = lista[start_secventa_maxima:start_secventa_maxima + lungime_maxima]
    
    return rezultat

        


def teste():
    # teste pentru secventa_egale
    assert secventa_egale([1, 1, 2, 2, 2, 3]) == [2, 2, 2]   # cea mai lunga secventa de egale e 3 de "2"
    assert secventa_egale([5, 5, 5, 5]) == [5, 5, 5, 5]      # toate egale
    assert secventa_egale([1, 2, 3, 4]) == [1]               # doar un element consecutiv
    
    # teste pentru secventa_suma_maxima
    assert secventa_suma_maxima([1, -2, 3, 5, -1, 2]) == [3, 5, -1, 2]   # suma maxima e 9
    assert secventa_suma_maxima([-3, -1, -2]) == [-1]                    # cel mai mare numar negativ
    assert secventa_suma_maxima([2, 4, -1, 2, -1]) == [2, 4, -1, 2]      # suma maxima e 7

    # teste pentru semne_contrare (semne alternante)
    assert semne_contrare([1, -2, 3, -4, 5]) == [1, -2, 3, -4, 5]           # semne alternante complete
    assert semne_contrare([2, 4, 6, 8]) == [2]                              # doar numere pozitive
    assert semne_contrare([-1, -3, -5, -7]) == [-1]                         # doar numere negative  
    assert semne_contrare([1, -2, 4, -6, 3]) == [1, -2, 4, -6, 3]           # toata secventa alternanta
    assert semne_contrare([2, -1, 4, -3, 6, -5]) == [2, -1, 4, -3, 6, -5]   # toata lista alternanta
    assert semne_contrare([]) == []                                          # lista goala
    assert semne_contrare([5]) == [5]                                        # un singur element
    assert semne_contrare([-3, 2, -1, 5]) == [-3, 2, -1, 5]                 # semne alternante complete
    assert semne_contrare([1, 2, -3, 4]) == [2, -3, 4]
    assert semne_contrare([-1,1,-1,1, 5,5,5,2, -2, 2, -2]) == [-1,1,-1,1]      # daca exista doua subsecvente de aceeasi lungime, returneaza prima          
    
    print("Toate testele au trecut cu succes!")





teste()
def meniu():
    # loop infinit
    while True:
        print("\nMeniu:")
        print("1. Secventa cu toate elementele egale")
        print("2. Secventa cu suma maxima")
        print("3. Secventa cu semne alternante")
        print("0. Iesire")
        opt = input("Alegeti optiunea: ")
        if opt == "1":
            lista = citire_lista()
            print(secventa_egale(lista))
        elif opt == "2":
            lista = citire_lista()
            print(secventa_suma_maxima(lista))
        elif opt == "3":
            lista = citire_lista()
            print(semne_contrare(lista))
        elif opt == "0":
            break
        else:
            print("Optiune invalida!")

meniu()
