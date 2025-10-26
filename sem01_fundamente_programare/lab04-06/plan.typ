#set page(margin: (x: 2cm, y: 2cm))
#set text(font: "Times New Roman", size: 12pt)

= PLAN NUMERE COMPLEXE - LAB 4-6
*Paul Tal*

== LISTA FUNCȚIONALITĂȚI

*F1.* Adaugă număr complex la sfârșitul listei  
*F2.* Inserează număr complex pe o poziție dată  
*F3.* Șterge element de pe o poziție dată  
*F4.* Șterge elementele de pe un interval de poziții  
*F5.* Înlocuiește toate aparițiile unui număr complex  
*F6.* Tipărește partea imaginară pentru un interval de poziții  
*F7.* Tipărește numerele cu modulul mai mic decât 10  
*F8.* Tipărește numerele cu modulul egal cu 10  
*F9.* Suma numerelor dintr-o subsecvență  
*F10.* Produsul numerelor dintr-o subsecvență  
*F11.* Lista sortată după partea imaginară  
*F12.* Filtrare partea reală primă  
*F13.* Filtrare după modul  
*F14.* Undo ultima operație

== PLANUL DE ITERAȚII

#table(
  columns: 2,
  [*Iterația*], [*Funcționalități*],
  [I1], [F1, F7, F8 + UI de bază],
  [I2], [F2, F3, F6, F9],
  [I3], [F4, F5, F10-F14]
)

== MODELAREA ITERAȚIEI 1

=== F1 - Adăugare număr

#table(
  columns: 3,
  [*Utilizator*], [*Program*], [*Descriere*],
  [Start aplicație], [Meniu principal], [Testare + meniu],
  [Selectează "1"], [Prompt input], ["Introduceti numarul complex"],
  [Tastează "3+4i"], ["Numar adaugat: 3+4i modul = 5.000"], [Confirmare],
  [Selectează "2"], [Lista: "0. 3+4i modul = 5.000"], [Afișare listă]
)

=== F7 - Filtrare modul < 10

#table(
  columns: 2,
  [*Input*], [*Output*],
  [Lista: [3+4i, 6+8i, 1+1i]], [Afișare numere cu modul < 10],
  [], ["3+4i modul = 5.000"],
  [], ["1+1i modul = 1.414"],
  [], ["Numere excluse: 6+8i modul = 10.000"]
)

=== F8 - Filtrare modul = 10

#table(
  columns: 2,
  [*Input*], [*Output*],
  [Lista: [6+8i, 3+4i]], [Căutare modul = 10],
  [], ["6+8i modul = 10.000"],
  [], ["Sugestii: 6+8i, 10+0i, 0+10i (dacă goală)"]
)

== TASK-URI ITERAȚIA 1

*T1.* Clasa ComplexNumber
- Constructor cu real, imaginary
- Metode: get_real(), get_imaginary(), get_string(), get_module()

*T2.* Calcularea modulului
- Formula: √(a² + b²)
- Teste cu diverse cazuri

*T3.* Storage-ul
- Clasa Storage pentru gestionarea listei  
- Metode: append_number(), get_numbers(), filtrări

*T4.* Parsarea input-ului
- Recunoaștere formate: "a+bi", "a-bi", "a", "bi", "i"
- Validare

*T5.* UI și meniu principal
- Meniu cu opțiuni
- Gestionare input/output

*T6.* Integrare și testare
- Test runner automat

== TESTE

=== ComplexNumber

#table(
  columns: 2,
  [*Input*], [*Output așteptat*],
  [ComplexNumber(3, 4)], [get_string() = "3+4i"],
  [ComplexNumber(5, -3)], [get_string() = "5-3i"],
  [ComplexNumber(3, 4)], [get_module() = 5.0]
)

=== Storage

#table(
  columns: 2,
  [*Operație*], [*Rezultat așteptat*],
  [append_number(3+4i)], [Lista: [3+4i]],
  [get_numbers_module_less_than(10)], [Returnează [3+4i, 1+1i]],
  [get_numbers_module_equal(10)], [Returnează [6+8i]]
)

=== Parser Input

#table(
  columns: 2,
  [*Input string*], [*Complex rezultat*],
  ["3+4i"], [ComplexNumber(3, 4)],
  ["5-2i"], [ComplexNumber(5, -2)],
  ["7"], [ComplexNumber(7, 0)],
  ["3i"], [ComplexNumber(0, 3)],
  ["i"], [ComplexNumber(0, 1)]
)

== ARHITECTURA

```
main.py
├── test_runner.py 
├── app.py 
├── ui.py 
├── menu_handler.py 
├── numar_complex.py 
└── storage.py 
```

== ITERAȚIA 2

- F2: Inserare pe poziție dată
- F3: Ștergere de pe poziție
- F6: Afișare părți imaginare din interval
- F9: Suma unei subsecvențe

== ITERAȚIA 3

- F4, F5: Operații avansate de ștergere/înlocuire
- F10, F11: Produs, sortare
- F12, F13: Filtrări avansate  
- F14: Undo functionality