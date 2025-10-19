import math
import os

def clear_screen():
    # sterge ecranul
    os.system('cls' if os.name == 'nt' else 'clear')

def creeaza_numar_complex(real, imaginar):
    # creeaza un nr complex ca tuplu
    return (real, imaginar)

def get_real(numar_complex):
    # partea reala
    return numar_complex[0]

def get_imaginar(numar_complex):
    # partea imaginara  
    return numar_complex[1]

def modul_numar_complex(numar_complex):
    # calculeaza modulul |a + bi| = sqrt(a^2 + b^2)
    real = get_real(numar_complex)
    imaginar = get_imaginar(numar_complex)
    return math.sqrt(real * real + imaginar * imaginar)

def adauga_numar_in_lista(lista, numar_complex):
    # adauga nr complex la sfarsit
    lista.append(numar_complex)

def afiseaza_parti_imaginare_interval(lista, start, end):
    # returneaza partile imaginare dintr-un interval  
    parti_imaginare = []
    for i in range(start, min(end + 1, len(lista))):
        parti_imaginare.append(get_imaginar(lista[i]))
    return parti_imaginare

def filtreaza_modul_mai_mic(lista, limita):
    # filtreaza numerele cu modulul mai mic decat limita
    rezultat = []
    for numar in lista:
        if modul_numar_complex(numar) < limita:
            rezultat.append(numar)
    return rezultat

def afiseaza_numar_complex(numar_complex):
    # afiseaza numarul in format a+bi sau a-bi
    real = get_real(numar_complex)
    imaginar = get_imaginar(numar_complex)
    
    if imaginar >= 0:
        return f"{real}+{imaginar}i"
    else:
        return f"{real}{imaginar}i"

def citeste_numar_complex():
    # citeste un numar complex de la utilizator
    print("\nIntroduceti un numar complex:")
    print("   Formate acceptate: 3+4i, 2-5i, 7i, -3i, 5, -2")
    print("   Exemple: 1+2i, 3-4i, 5i, 6, -7+8i")
    
    while True:
        try:
            input_str = input("Numarul complex: ").strip().replace(" ", "")
            
            if not input_str:
                print("Eroare: Nu ati introdus nimic! Va rog sa introduceti un numar.")
                continue
            
            # verifica daca contine caractere invalide
            caractere_valide = set("0123456789+-i.")
            if not all(c in caractere_valide for c in input_str):
                print("Eroare: Caractere invalide! Folositi doar cifre, +, -, i si punctul decimal.")
                continue
            
            # cazul in care nu avem 'i' - doar partea reala
            if 'i' not in input_str:
                try:
                    real = float(input_str)
                    return creeaza_numar_complex(real, 0)
                except ValueError:
                    print("Eroare: Formatul nu este corect pentru numarul real!")
                    continue
            
            # elimina 'i' de la sfarsit
            if not input_str.endswith('i'):
                print("Eroare: Partea imaginara trebuie sa se termine cu 'i'!")
                continue
                
            input_str = input_str[:-1]  # elimina 'i'
            
            # cazul in care avem doar 'i' sau '-i' sau '+i'
            if input_str == '' or input_str == '+':
                return creeaza_numar_complex(0, 1)
            elif input_str == '-':
                return creeaza_numar_complex(0, -1)
            
            # verifica daca avem doar partea imaginara (ex: 5i, -3i)
            if '+' not in input_str and input_str.count('-') <= 1 and input_str.startswith('-'):
                # doar partea imaginara negativa
                try:
                    imaginar = float(input_str)
                    return creeaza_numar_complex(0, imaginar)
                except ValueError:
                    print("Eroare: Formatul partii imaginare nu este corect!")
                    continue
            elif '+' not in input_str and '-' not in input_str:
                # doar partea imaginara pozitiva
                try:
                    imaginar = float(input_str)
                    return creeaza_numar_complex(0, imaginar)
                except ValueError:
                    print("Eroare: Formatul partii imaginare nu este corect!")
                    continue
            
            # cazul general: a+bi sau a-bi
            # gaseste ultimul + sau - care separa partile reala si imaginara
            pos_plus = input_str.rfind('+')
            pos_minus = input_str.rfind('-')
            
            if pos_plus == -1 and pos_minus == -1:
                print("Eroare: Nu s-a gasit separatorul intre partea reala si imaginara!")
                continue
            
            # determina pozitia separatorului
            if pos_plus > pos_minus:
                separator_pos = pos_plus
                separator = '+'
            else:
                separator_pos = pos_minus
                separator = '-'
            
            # verifica daca separatorul nu este la inceput
            if separator_pos == 0:
                print("Eroare: Formatul nu este corect! Partea reala lipseste.")
                continue
            
            try:
                real_str = input_str[:separator_pos]
                imaginar_str = input_str[separator_pos+1:]
                
                real = float(real_str)
                
                if imaginar_str == '':
                    imaginar = 1 if separator == '+' else -1
                else:
                    imaginar = float(imaginar_str)
                    if separator == '-':
                        imaginar = -imaginar
                
                return creeaza_numar_complex(real, imaginar)
                
            except ValueError:
                print("Eroare: Una dintre parti nu este un numar valid!")
                continue
            
        except KeyboardInterrupt:
            print("\nOperatia a fost anulata.")
            return None
        except Exception as e:
            print(f"Eroare neasteptata: {e}")
            print("Va rog sa incercati din nou cu un format valid (ex: 3+4i, 2-5i).")

def afiseaza_lista(lista):
    if not lista:
        print("📭 Lista este goala.")
        return
        
    print(f"📋 Lista de numere complexe ({len(lista)} elemente):")
    print("─" * 45)
    for i, numar in enumerate(lista):
        modul = modul_numar_complex(numar)
        print(f"{i:2d}. {afiseaza_numar_complex(numar):>10s} → |z| = {modul:.3f}")
    print("─" * 45)

def pauza():
    # pauza pentru a citi rezultatul
    input("\nApasati Enter pentru a continua...")

def afiseaza_meniu():
    clear_screen()
    print("╔" + "═" * 58 + "╗")
    print("║" + "    APLICATIE NUMERE COMPLEXE - ITERATIA 1".center(58) + "║")
    print("╠" + "═" * 58 + "╣")
    print("║                                                          ║")
    print("║  📋 GESTIUNE LISTA:                                      ║")
    print("║     1. Adauga numar complex la sfarsit                   ║")
    print("║     2. Afiseaza lista curenta                            ║")
    print("║                                                          ║")
    print("║  🔍 CAUTARE & AFISARE:                                   ║")
    print("║     3. Afiseaza partile imaginare din interval           ║")
    print("║     4. Afiseaza numere cu modulul < 10                   ║")
    print("║     5. Afiseaza numere cu modulul = 10                   ║")
    print("║                                                          ║")
    print("║  ❓ AJUTOR:                                              ║")
    print("║     h. Afiseaza explicatii si exemple                    ║")
    print("║                                                          ║")
    print("║     0. Iesire din aplicatie                              ║")
    print("║                                                          ║")
    print("╚" + "═" * 58 + "╝")
    print()

def ui_adauga_numar_complex(lista):
    try:
        clear_screen()
        print("╔" + "═" * 50 + "╗")
        print("║" + "        ADAUGARE NUMAR COMPLEX".center(50) + "║")
        print("╚" + "═" * 50 + "╝")
        print()
        
        numar = citeste_numar_complex()
        if numar is None:  # utilizatorul a anulat
            return
            
        adauga_numar_in_lista(lista, numar)
        
        print(f"\n✅ Succes! Numarul {afiseaza_numar_complex(numar)} a fost adaugat!")
        modul = modul_numar_complex(numar)
        print(f"   Modulul: |z| = {modul:.3f}")
        
        print(f"\n📊 Lista actualizata ({len(lista)} elemente):")
        print("─" * 45)
        for i, nr in enumerate(lista[-3:], max(0, len(lista)-3)):
            mod = modul_numar_complex(nr)
            if i == len(lista) - 1:  # ultimul element (nou adaugat)
                print(f"{i:2d}. {afiseaza_numar_complex(nr):>10s} -> |z| = {mod:.3f} ← NOU")
            else:
                print(f"{i:2d}. {afiseaza_numar_complex(nr):>10s} -> |z| = {mod:.3f}")
        
        if len(lista) > 3:
            print(f"   ... și încă {len(lista)-3} elemente anterioare")
        
        pauza()
    except Exception as e:
        print(f"❌ Eroare la adaugarea numarului: {e}")
        pauza()

def ui_afiseaza_parti_imaginare_interval(lista):
    if not lista:
        clear_screen()
        print("❌ Lista este goala! Nu exista numere pentru afisare.")
        pauza()
        return
    
    clear_screen()
    print("╔" + "═" * 55 + "╗")
    print("║" + "    AFISARE PARTI IMAGINARE DIN INTERVAL".center(55) + "║")
    print("╚" + "═" * 55 + "╝")
    print()
    
    print(f"📋 Lista curenta are {len(lista)} elemente (indexuri 0-{len(lista)-1})")
    print("─" * 55)
    for i, numar in enumerate(lista):
        modul = modul_numar_complex(numar)
        print(f"{i:2d}. {afiseaza_numar_complex(numar):>10s} -> |z| = {modul:.3f}")
    print("─" * 55)
    
    while True:
        try:
            print(f"\n🔢 Introduceti intervalul de pozitii:")
            start_str = input(f"   Pozitia de inceput (0-{len(lista)-1}): ").strip()
            
            if not start_str:
                print("❌ Eroare: Nu ati introdus pozitia de inceput!")
                continue
                
            start = int(start_str)
            
            if start < 0 or start >= len(lista):
                print(f"❌ Eroare: Pozitia de inceput trebuie sa fie intre 0 si {len(lista)-1}!")
                continue
            
            end_str = input(f"   Pozitia de sfarsit ({start}-{len(lista)-1}): ").strip()
            
            if not end_str:
                print("❌ Eroare: Nu ati introdus pozitia de sfarsit!")
                continue
                
            end = int(end_str)
            
            if end < start or end >= len(lista):
                print(f"❌ Eroare: Pozitia de sfarsit trebuie sa fie intre {start} si {len(lista)-1}!")
                continue
                
            parti_imaginare = afiseaza_parti_imaginare_interval(lista, start, end)
            
            print(f"\n✅ Partile imaginare din intervalul [{start}, {end}]:")
            print("   ", end="")
            for i, parte_imag in enumerate(parti_imaginare):
                if i > 0:
                    print(", ", end="")
                print(f"{parte_imag:g}", end="")
            print()
            
            print(f"\n📊 Detalii pentru intervalul selectat:")
            print("─" * 45)
            for i in range(start, end + 1):
                parte_imag = get_imaginar(lista[i])
                print(f"{i:2d}. {afiseaza_numar_complex(lista[i]):>10s} → partea imag: {parte_imag:g}")
            
            pauza()
            break
            
        except ValueError:
            print("❌ Eroare: Va rog introduceti doar numere intregi!")
        except KeyboardInterrupt:
            print("\n🛑 Operatia a fost anulata.")
            break
        except Exception as e:
            print(f"❌ Eroare neasteptata: {e}")
            pauza()
            break

def ui_afiseaza_numere_modul_mic(lista):
    if not lista:
        clear_screen()
        print("❌ Lista este goala! Nu exista numere pentru filtrare.")
        pauza()
        return
    
    clear_screen()
    print("╔" + "═" * 50 + "╗")
    print("║" + "    NUMERE CU MODULUL < 10".center(50) + "║")
    print("╚" + "═" * 50 + "╝")
    print()
        
    numere_filtrate = filtreaza_modul_mai_mic(lista, 10)
    
    if not numere_filtrate:
        print("❌ Nu exista numere cu modulul mai mic decat 10 in lista curenta.")
        print(f"\n📋 Lista curenta ({len(lista)} elemente):")
        print("─" * 45)
        for i, numar in enumerate(lista):
            modul = modul_numar_complex(numar)
            print(f"{i:2d}. {afiseaza_numar_complex(numar):>10s} -> |z| = {modul:.3f}")
        pauza()
        return
        
    print(f"✅ Numere cu modulul < 10: {len(numere_filtrate)} din {len(lista)} total")
    print("═" * 50)
    
    for numar in numere_filtrate:
        modul = modul_numar_complex(numar)
        print(f"   {afiseaza_numar_complex(numar):>10s} → |z| = {modul:.3f} < 10 ✓")
    
    print("═" * 50)
    
    if len(numere_filtrate) < len(lista):
        print(f"\n📊 Numere excluse (|z| ≥ 10): {len(lista) - len(numere_filtrate)}")
        print("─" * 45)
        for numar in lista:
            modul = modul_numar_complex(numar)
            if modul >= 10:
                print(f"   {afiseaza_numar_complex(numar):>10s} → |z| = {modul:.3f} ≥ 10")
    
    pauza()

def ui_afiseaza_numere_modul_egal(lista):
    if not lista:
        clear_screen()
        print("❌ Lista este goala! Nu exista numere pentru filtrare.")
        pauza()
        return
    
    clear_screen()
    print("╔" + "═" * 50 + "╗")
    print("║" + "    NUMERE CU MODULUL = 10".center(50) + "║")
    print("╚" + "═" * 50 + "╝")
    print()
        
    numere_filtrate = []
    for numar in lista:
        modul = modul_numar_complex(numar)
        if abs(modul - 10) < 0.001:  # comparatie cu toleranta pentru floating point
            numere_filtrate.append(numar)
    
    if not numere_filtrate:
        print("❌ Nu exista numere cu modulul egal cu 10 in lista curenta.")
        print(f"\n📋 Lista curenta ({len(lista)} elemente):")
        print("─" * 45)
        for i, numar in enumerate(lista):
            modul = modul_numar_complex(numar)
            print(f"{i:2d}. {afiseaza_numar_complex(numar):>10s} -> |z| = {modul:.3f}")
        
        print(f"\n💡 Hint: Pentru modul = 10, incercati numere ca:")
        print("   • 6+8i  (modulul = √(36+64) = 10)")
        print("   • 10+0i (modulul = 10)")
        print("   • 0+10i (modulul = 10)")
        pauza()
        return
        
    print(f"✅ Numere cu modulul = 10: {len(numere_filtrate)} din {len(lista)} total")
    print("═" * 50)
    
    for numar in numere_filtrate:
        modul = modul_numar_complex(numar)
        print(f"   {afiseaza_numar_complex(numar):>10s} → |z| = {modul:.3f} = 10 ✓")
    
    print("═" * 50)
    pauza()

def ui_afiseaza_ajutor():
    clear_screen()
    print("╔" + "═" * 68 + "╗")
    print("║" + "              GHID DE UTILIZARE.    ".center(68) + "║")
    print("╠" + "═" * 68 + "╣")
    print("║                                                                    ║")
    print("║  📝 FORMATE ACCEPTATE PENTRU NUMERE COMPLEXE:                      ║")
    print("║                                                                    ║")
    print("║     • Numar complet:     3+4i, 2-5i, -1+7i, -3-2i                  ║")
    print("║     • Doar partea reala: 5, -3, 0                                  ║")
    print("║     • Doar partea imag:  4i, -7i, i, -i                            ║")
    print("║     • Zero:              0, 0+0i                                   ║")
    print("║                                                                    ║")
    print("║  🔢 EXEMPLE PRACTICE:                                              ║")
    print("║                                                                    ║")
    print("║     3+4i  →  modulul = √(3² + 4²) = √25 = 5                        ║")
    print("║     6+8i  →  modulul = √(6² + 8²) = √100 = 10                      ║")
    print("║     5-12i →  modulul = √(5² + 12²) = √169 = 13                     ║")
    print("║                                                                    ║")
    print("║  ⚠️  REGULI IMPORTANTE:                                             ║")
    print("║                                                                    ║")
    print("║     • Nu folositi spatii in numere: 3+4i (corect), 3 + 4i (gresit) ║")
    print("║     • Partea imaginara se termina cu 'i'                           ║")
    print("║     • Pentru intervaluri: pozitiile incep de la 0                  ║")
    print("║                                                                    ║")
    print("╚" + "═" * 68 + "╝")
    pauza()

def main():
    # functia principala a aplicatiei
    lista_numere = []
    
    while True:
        afiseaza_meniu()
        
        try:
            optiune = input("Alegeti o optiune: ").strip().lower()
            
            if not optiune:
                print("Eroare: Nu ati ales o optiune! Va rog sa introduceti o optiune valida.")
                pauza()
                continue
            
            if optiune == '1':
                ui_adauga_numar_complex(lista_numere)
            elif optiune == '2':
                clear_screen()
                print("═" * 60)
                print("                    LISTA CURENTA")
                print("═" * 60)
                afiseaza_lista(lista_numere)
                pauza()
            elif optiune == '3':
                ui_afiseaza_parti_imaginare_interval(lista_numere)
            elif optiune == '4':
                ui_afiseaza_numere_modul_mic(lista_numere)
            elif optiune == '5':
                ui_afiseaza_numere_modul_egal(lista_numere)
            elif optiune == 'h':
                ui_afiseaza_ajutor()
            elif optiune == '0':
                clear_screen()
                print("╔" + "═" * 40 + "╗")
                print("║" + "   Multumim pentru utilizare!   ".center(40) + "║")
                print("║" + "          La revedere!          ".center(40) + "║")
                print("╚" + "═" * 40 + "╝")
                break
            else:
                print(f"\n❌ Optiunea '{optiune}' nu este valida!")
                print("Optiuni disponibile: 1, 2, 3, 4, 5, h, 0")
                print("Apasati 'h' pentru explicatii detaliate.")
                pauza()
                
        except KeyboardInterrupt:
            clear_screen()
            print("\n🛑 Aplicatia a fost inchisa de utilizator.")
            print("La revedere!")
            break
        except Exception as e:
            print(f"❌ Eroare neasteptata: {e}")
            print("Se incearca reluarea aplicatiei...")
            pauza()

# functii de test
def test_creare_numar_complex():
    # testeaza crearea unui numar complex
    nr = creeaza_numar_complex(3, 4)
    assert get_real(nr) == 3
    assert get_imaginar(nr) == 4

def test_modul_numar_complex():
    # testeaza calculul modulului
    nr1 = creeaza_numar_complex(3, 4)  # modul = 5
    assert modul_numar_complex(nr1) == 5
    
    nr2 = creeaza_numar_complex(0, 0)  # modul = 0
    assert modul_numar_complex(nr2) == 0
    
    nr3 = creeaza_numar_complex(1, 0)  # modul = 1
    assert modul_numar_complex(nr3) == 1

def test_adauga_numar_in_lista():
    # testeaza adaugarea unui numar in lista
    lista = []
    nr = creeaza_numar_complex(2, 3)
    adauga_numar_in_lista(lista, nr)
    assert len(lista) == 1
    assert get_real(lista[0]) == 2
    assert get_imaginar(lista[0]) == 3

def test_afiseaza_parti_imaginare_interval():
    # testeaza afisarea partilor imaginare dintr-un interval
    lista = []
    adauga_numar_in_lista(lista, creeaza_numar_complex(1, 2))
    adauga_numar_in_lista(lista, creeaza_numar_complex(3, 4))
    adauga_numar_in_lista(lista, creeaza_numar_complex(5, 6))
    
    result = afiseaza_parti_imaginare_interval(lista, 0, 1)
    assert result == [2, 4]
    
    result = afiseaza_parti_imaginare_interval(lista, 1, 2)
    assert result == [4, 6]

def test_filtreaza_modul_mai_mic():
    # testeaza filtrarea numerelor cu modulul mai mic decat 10
    lista = []
    adauga_numar_in_lista(lista, creeaza_numar_complex(3, 4))  # modul = 5
    adauga_numar_in_lista(lista, creeaza_numar_complex(6, 8))  # modul = 10
    adauga_numar_in_lista(lista, creeaza_numar_complex(9, 12)) # modul = 15
    
    result = filtreaza_modul_mai_mic(lista, 10)
    assert len(result) == 1
    assert get_real(result[0]) == 3
    assert get_imaginar(result[0]) == 4

def ruleaza_toate_testele():
    # ruleaza toate testele
    test_creare_numar_complex()
    test_modul_numar_complex()
    test_adauga_numar_in_lista()
    test_afiseaza_parti_imaginare_interval()
    test_filtreaza_modul_mai_mic()
    print("Toate testele au trecut!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        ruleaza_toate_testele()
    else:
        main()