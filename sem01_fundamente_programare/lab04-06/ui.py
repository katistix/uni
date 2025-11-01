import os
import numar_complex

def clear_screen():
    # sterge ecranul
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    print(
"""APLICATIE NUMERE COMPLEXE

1. Adauga numar complex la sfarsitul listei
2. Afiseaza lista curenta
3. Afiseaza parti imaginare din interval
4. Afiseaza numere cu modulul mai mic decat 10
5. Afiseaza numere cu modulul egal cu 10
6. Insereaza numar complex la pozitie data
7. Sterge numar de la pozitie data
8. Suma numerelor dintr-o subsecventa
9. Sterge numere dintr-un interval de pozitii
10. Inlocuieste toate aparitiile unui numar complex
11. Produsul numerelor dintr-o subsecventa
12. Afiseaza lista sortata dupa partea imaginara
13. Filtrare numere cu partea reala prima
14. Filtrare numere dupa modul
15. Undo ultima operatie
h. Ajutor
0. Iesire

""")
    

def get_menu_option():
    val = input(">> ")
    return val

def get_complex_number_input():
    while True:
        try:
            input_str = input("Introduceti numarul complex (format: a+bi sau a-bi): ")
            return parse_complex_number(input_str)
        except ValueError as e:
            print(f"Eroare: {e}")
            print("Exemple valide: 3+4i, 5-2i, 7+0i, 0+3i")

def parse_complex_number(input_str: str):
    input_str = input_str.replace(" ", "")
    
    if input_str == "i":
        return numar_complex.ComplexNumber(0, 1)
    if input_str == "-i":
        return numar_complex.ComplexNumber(0, -1)
    
    if not input_str.endswith("i"):
        raise ValueError("Formatul trebuie sa se termine cu 'i'")
    
    input_str = input_str[:-1]  # remove 'i'
    
    if '+' in input_str:
        parts = input_str.split('+')
        if len(parts) != 2:
            raise ValueError("Format invalid")
        real = int(parts[0])
        imaginary = int(parts[1]) if parts[1] else 1
    elif '-' in input_str[1:]:  # skip first char for negative real
        idx = input_str.rfind('-')
        real = int(input_str[:idx])
        imaginary = int(input_str[idx:]) if input_str[idx:] != '-' else -1
    else:
        if input_str == '':
            real, imaginary = 0, 1
        elif input_str == '-':
            real, imaginary = 0, -1
        else:
            try:
                real = int(input_str)
                imaginary = 0
            except ValueError:
                imaginary = int(input_str) if input_str not in ['', '-'] else (1 if input_str == '' else -1)
                real = 0
    
    return numar_complex.ComplexNumber(real, imaginary)

def get_interval_input(max_index):
    while True:
        try:
            start = int(input(f"Introduceti indexul de start (0-{max_index}): "))
            end = int(input(f"Introduceti indexul de sfarsit (0-{max_index}): "))
            
            if start < 0 or end > max_index or start > end:
                print(f"Interval invalid. Trebuie sa fie intre 0 si {max_index}, cu start <= end")
                continue
            
            return start, end
        except ValueError:
            print("Va rog introduceti numere intregi valide")

def show_numbers_with_modules(numbers):
    if not numbers:
        print("Lista este goala")
        return
    
    print("\nLista curenta:")
    for i, number in enumerate(numbers):
        module = number.get_module()
        print(f"{i}. {number.get_string()} modul = {module:.3f}")

def show_imaginary_parts(numbers, parts, start, end):
    print(f"\nPartile imaginare pentru intervalul [{start}, {end}]:")
    for i in range(len(parts)):
        idx = start + i
        print(f"{idx}. {numbers[idx].get_string()} partea imag: {parts[i]}")

def show_filtered_numbers(numbers, title):
    print(f"\n{title}:")
    if not numbers:
        print("Nu au fost gasite numere care indeplinesc conditia")
        return
    
    for number in numbers:
        module = number.get_module()
        print(f"{number.get_string()} modul = {module:.3f}")

def show_help():
    print("""
GHID DE UTILIZARE

Format numere complexe acceptate:
- 3+4i (partea reala 3, partea imaginara 4)
- 5-2i (partea reala 5, partea imaginara -2)  
- 7+0i sau 7 (doar partea reala)
- 0+3i sau 3i (doar partea imaginara)
- i (echivalent cu 0+1i)

Exemple de module:
- 3+4i are modulul = 5.000
- 6+8i are modulul = 10.000  
- 0+1i are modulul = 1.000

Operatii disponibile:
1. Adauga numere complexe la sfarsitul listei
2. Vizualizeaza toate numerele cu modulele calculate
3. Afiseaza partile imaginare pentru un interval de pozitii
4. Filtreaza numerele cu modulul mai mic decat 10
5. Filtreaza numerele cu modulul exact egal cu 10
""")

def get_position_input(max_index, operation_name):
    while True:
        try:
            position = int(input(f"Introduceti pozitia pentru {operation_name} (0-{max_index}): "))
            
            if position < 0 or position > max_index:
                print(f"Pozitie invalida. Trebuie sa fie intre 0 si {max_index}")
                continue
            
            return position
        except ValueError:
            print("Va rog introduceti un numar intreg valid")

def show_sum_result(numbers, result_sum, start, end):
    print(f"\nSuma numerelor din intervalul [{start}, {end}]:")
    print("Numere incluse:")
    for i in range(start, end + 1):
        print(f"  {i}. {numbers[i].get_string()}")
    print(f"Suma: {result_sum.get_string()} (modul = {result_sum.get_module():.3f})")


def show_product_result(numbers, result_product, start, end):
    print(f"\nProdusul numerelor din intervalul [{start}, {end}]:")
    print("Numere incluse:")
    for i in range(start, end + 1):
        print(f"  {i}. {numbers[i].get_string()}")
    print(f"Produs: {result_product.get_string()} (modul = {result_product.get_module():.3f})")


def show_sorted_numbers(sorted_numbers, title):
    print(f"\n{title}:")
    if not sorted_numbers:
        print("Lista este goala")
        return
    
    for i, number in enumerate(sorted_numbers):
        module = number.get_module()
        print(f"{i}. {number.get_string()} modul = {module:.3f} (imaginara = {number.imaginary})")


def get_operator_input():
    """Get comparison operator from user"""
    while True:
        operator = input("Introduceti operatorul de comparatie (<, =, >): ").strip()
        if operator in ['<', '=', '>']:
            return operator
        print("Operator invalid. Va rog introduceti <, = sau >")


def get_float_input(prompt):
    """Get float value from user with validation"""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Va rog introduceti un numar valid")


def show_filter_result(operation_name, removed_count, remaining_count):
    """Show result of a filter operation"""
    print(f"\n{operation_name}:")
    if removed_count > 0:
        print(f"Eliminate {removed_count} numere")
        print(f"Raman {remaining_count} numere in lista")
    else:
        print("Nu au fost eliminate numere")


def show_replacement_result(old_number, new_number, replacement_count):
    """Show result of replacement operation"""
    print(f"\nInlocuire aparitii:")
    if replacement_count > 0:
        print(f"Inlocuite {replacement_count} aparitii ale lui {old_number.get_string()} cu {new_number.get_string()}")
    else:
        print(f"Nu au fost gasite aparitii ale lui {old_number.get_string()}")


def show_undo_result(success):
    """Show result of undo operation"""
    if success:
        print("\nUndo efectuat cu succes")
    else:
        print("\nNu exista operatii pentru undo")