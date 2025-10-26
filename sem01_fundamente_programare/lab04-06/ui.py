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