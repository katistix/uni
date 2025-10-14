def citire_lista():
    sir = input("Introduceti numere separate prin spatiu: ")
    lista = []
    for x in sir.split():
        lista.append(int(x))  # conversie la int
    return lista

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
    
    # afisare cea mai lunga secventa si return in caz ca dorim sa o folosim altundeva
    print("Secventa egala:", cea_mai_lunga)
    return cea_mai_lunga

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

    # pentru fiecare element din lista
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

    # afisare si return
    print("Secventa suma maxima:", rezultat)
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
    
    print("Toate testele au trecut cu succes!")


def meniu():
    # loop infinit
    while True:
        print("\nMeniu:")
        print("1. Secventa cu toate elementele egale")
        print("2. Secventa cu suma maxima")
        print("9. Ruleaza testele")
        print("0. Iesire")
        opt = input("Alegeti optiunea: ")
        if opt == "1":
            lista = citire_lista()
            secventa_egale(lista)
        elif opt == "2":
            lista = citire_lista()
            secventa_suma_maxima(lista)
        elif opt == "9":
            teste()
        elif opt == "0":
            break
        else:
            print("Optiune invalida!")

meniu()
