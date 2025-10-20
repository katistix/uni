#set page(margin: (x: 2cm, y: 2cm))
#set text(font: "Times New Roman", size: 12pt)
#set par(justify: true, leading: 0.8em)

= Plan de iterare proiect FP lab04-06

*Student:* Paul Tal  
*Problemă:* P1. Numere complexe  
*Data:* Octombrie 2025

== Enunțul problemei

Creați un program care lucrează cu numere complexe (a + bi). Programul gestionează o listă de numere complexe și permite efectuarea repetată a următoarelor acțiuni:

1. Adaugă număr în listă
2. Modifică elemente din listă  
3. Căutare numere
4. Operații cu numerele din listă
5. Filtrare
6. Undo

== Lista de funcționalități

=== 1. Adăugare numere
- F1. Adaugă număr complex la sfârșitul listei
- F2. Inserare număr complex pe o poziție dată

=== 2. Modificare elemente  
- F3. Șterge element de pe o poziție dată
- F4. Șterge elementele de pe un interval de poziții
- F5. Înlocuiește toate aparițiile unui număr complex cu un alt număr complex

=== 3. Căutare și afișare
- F6. Tipărește partea imaginară pentru numerele din listă (interval de poziții)
- F7. Tipărește toate numerele complexe care au modulul mai mic decât 10
- F8. Tipărește toate numerele complexe care au modulul egal cu 10

=== 4. Operații matematice
- F9. Suma numerelor dintr-o subsecvență dată
- F10. Produsul numerelor dintr-o subsecvență dată  
- F11. Tipărește lista sortată descrescător după partea imaginară

=== 5. Filtrare
- F12. Filtrare parte reală prim – elimină din listă numerele cu partea reală prim
- F13. Filtrare modul – elimină din listă numerele cu modulul <, = sau > decât un număr dat

=== 6. Funcționalități speciale
- F14. Undo – reface ultima operație  

== Plan de iterații

#table(
  columns: (1fr, 3fr),
  align: left,
  stroke: 0.7pt,
  fill: (rgb("f0f0f0"), none) * 2,
  table.header[*Iterația*][*Funcționalități planificate*],
  [*I1*], [
    • F1. Adaugă număr complex la sfârșitul listei \ 
    • F6. Tipărește partea imaginară pentru numere din interval \ 
    • F7. Tipărește numerele cu modulul mai mic decât 10 \
    • F8. Tipărește numerele cu modulul egal cu 10 \
    • Afișare listă curentă
  ],
  [*I2*], [
    • F2. Inserare număr complex pe poziție \ 
    • F3. Șterge element de pe poziție \ 
    • F9. Suma numerelor dintr-o subsecvență
  ],
  [*I3*], [
    • F4. Șterge elemente din interval \ 
    • F5. Înlocuiește aparițiile unui număr \ 
    • F14. Undo – reface ultima operație
  ]
)

== Iterația 1 - Modelarea funcționalităților

=== F1. Adaugă număr complex la sfârșitul listei

*Scenariu de rulare pentru adăugarea numerelor complexe:*

#table(
  columns: (1fr, 2fr, 2fr),
  align: left,
  stroke: 0.5pt,
  fill: (rgb("f8f8f8"), none, none) * 3,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [1], [Meniu afișat], [Alege "1. Adaugă număr complex"],
  [3+4i], [Interfață pentru introducerea numerelor], [Introduce numărul cu validare],
  [], [Confirmare cu modul calculat și listă actualizată], [Afișează succesul operației],
  [1], [Revenire la meniu principal], [Alege din nou adăugarea], 
  [6+8i], [Același workflow], [Introduce număr cu modul = 10],
  [], [Lista: \[(3, 4), (6, 8)\] cu module afișate], [Confirmă cu indicarea modulului]
)

=== F2. Afișare listă curenta

*Scenariu de rulare pentru vizualizarea listei:*

#table(
  columns: (1fr, 2fr, 2fr),
  align: left,
  stroke: 0.5pt,
  fill: (rgb("f8f8f8"), none, none) * 3,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [2], [Meniu principal], [Alege "2. Afișează lista curentă"],
  [], [Lista formatată cu module], [Afișează toate numerele cu calculul modulului],
  [], [Format: "0. 3+4i modul = 5.000"], [Informații despre fiecare element]
)

=== F6. Tipărește partea imaginară pentru numere din interval

*Interfață pentru gestionarea intervalelor:*

#table(
  columns: (1fr, 2fr, 2fr),
  align: left,
  stroke: 0.5pt,
  fill: (rgb("f8f8f8"), none, none) * 3,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [3], [Meniu], [Alege "3. Afișează părți imaginare"],
  [], [Lista cu indexuri], [Afișează toate elementele cu pozițiile],
  [0 1], [Validare interval], [Introduce interval cu verificări],
  [], [Părți imaginare: 4, -5], [Afișează rezultatul și elementele originale],
  [], [Mapare: "0. 3+4i partea imag: 4"], [Corelația dintre pozițiile și rezultate]
)

=== F7. Tipărește numerele cu modulul mai mic decât 10

*Interfață pentru filtrarea după modul:*

#table(
  columns: (1fr, 2fr, 2fr),
  align: left,
  stroke: 0.5pt,
  fill: (rgb("f8f8f8"), none, none) * 3,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [4], [Meniu], [Alege "4. Numere cu modul < 10"],
  [], [Analiză și categorisare], [Filtrează și grupează rezultatele],
  [], [Numere incluse: 3+4i (modul=5)], [Afișează numerele care îndeplinesc condiția],
  [], [Numere excluse: 6+8i (modul=10)], [Arată și numerele care nu îndeplinesc condiția]
)

=== F8. Tipărește numerele cu modulul egal cu 10

*Funcționalitate pentru modulul egal cu 10:*

#table(
  columns: (1fr, 2fr, 2fr),
  align: left,
  stroke: 0.5pt,
  fill: (rgb("f8f8f8"), none, none) * 3,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [5], [Meniu cu funcționalitatea], [Alege "5. Numere cu modul = 10"],
  [], [Căutare pentru numere reale], [Găsește numerele cu modul exact 10],
  [], [Rezultat: 6+8i modul = 10.000 = 10], [Afișează cu confirmarea egalității],
  [], [Sugestii dacă nu găsește rezultate], [Oferă exemple pentru modul = 10]
)

=== Ghid de utilizare integrat

*Funcționalitate pentru ajutor:*

#table(
  columns: (1fr, 2fr, 2fr),
  align: left,
  stroke: 0.5pt,
  fill: (rgb("f8f8f8"), none, none) * 3,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [h], [Meniu cu opțiune de ajutor], [Alege "h. Afișează explicații"],
  [], [Ghid cu formate acceptate], [Arată exemple și reguli],
  [], [Exemple de module: 3+4i modul = 5], [Explică calculul modulului cu exemple],
  [], [Reguli și formatare], [Instrucțiuni pentru introducerea datelor]
)

== Lista de activități (Tasks) pentru Iterația 1

+ Creează structura de date pentru reprezentarea numerelor complexe
+ Implementează funcția de adăugare număr complex în listă
+ Implementează funcția de calculare a modulului unui număr complex
+ Implementează funcția de tipărire părți imaginare din interval
+ Implementează funcția de filtrare numere cu modul < 10
+ Implementează funcția de filtrare numere cu modul = 10
+ Implementează meniul principal cu opțiuni
+ Implementează interfețe pentru fiecare funcționalitate
+ Implementează sistem de ajutor cu ghid de utilizare
+ Implementează validare și mesaje de eroare
+ Implementează afișare cu formatare
+ Implementează funcții de test pentru toate funcționalitățile
+ Integrarea tuturor componentelor în aplicația principală

== Aspecte tehnice pentru Iterația 1

=== Design meniu

- Organizare pe categorii: Gestiune listă, Căutare și Afișare, Ajutor
- Numerotare: 1-5 pentru funcționalități principale, h pentru ajutor, 0 pentru ieșire  
- Interfață: Utilizare caractere pentru borduri
- Claritate: Opțiuni pentru fiecare categorie

=== Funcționalități implementate

- F8. Numere cu modul = 10: Completează cerințele din problemă
- Ghid de utilizare: Explicații și exemple practice
- Validare: Mesaje de eroare cu sugestii de rezolvare

=== Experiența utilizatorului

- Feedback vizual: Confirmări și indicatori de stare
- Informații contextuale: Module calculate și afișate pentru fiecare număr
- Navigare: Instrucțiuni la fiecare pas
- Recuperare din erori: Mesaje cu exemple

== Cazuri de testare pentru Iterația 1

=== Adăugare numere complexe

#table(
  columns: (2fr, 2fr),
  align: left,
  stroke: 0.5pt,
  fill: (rgb("f0f8ff"), none) * 2,
  table.header[*Input*][*Output așteptat*],
  [3+4i], [Confirmare cu modul = 5.000, listă actualizată],
  [6+8i], [Confirmare cu modul = 10.000, listă cu 2 elemente],
  [0+0i], [Confirmare cu modul = 0.000, listă cu 3 elemente],
  [i], [Confirmare cu modul = 1.000 (0+1i)],
  [Format invalid], [Mesaj de eroare cu exemple]
)

=== Părți imaginare din interval

#table(
  columns: (2fr, 2fr),
  align: left,
  stroke: 0.5pt,
  fill: (rgb("f0f8ff"), none) * 2,
  table.header[*Input (interval)*][*Output așteptat*],
  [0, 1], [4, -5 + mapare clară cu elementele originale],
  [1, 2], [-5, 0 + verificare corectitudine],
  [0, 2], [4, -5, 0 + afișare completă],
  [Interval invalid], [Mesaj de eroare cu limitele corecte]
)

=== Filtrare după modul

#table(
  columns: (2fr, 2fr),
  align: left,
  stroke: 0.5pt,
  fill: (rgb("f0f8ff"), none) * 2,
  table.header[*Operație*][*Rezultat așteptat*],
  [Modul < 10 pentru \[(3,4), (6,8), (9,12)\]], [(3,4) inclus + (6,8), (9,12) excluse],
  [Modul = 10 pentru \[(3,4), (6,8), (0,10)\]], [(6,8), (0,10) găsite cu confirmarea egalității],
  [Listă goală], [Mesaj că lista este goală],
  [Fără rezultate modul = 10], [Sugestii: 6+8i, 10+0i, 0+10i]
)
