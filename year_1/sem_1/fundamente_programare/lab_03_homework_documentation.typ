#set page(margin: (x: 2cm, y: 2cm))
#set text(font: "Times New Roman", size: 12pt)
#set par(justify: true, leading: 0.8em)

= Lab 3 - Fundamentele programarii

Se predă in saptamana 3.

Aplicatie cu meniu consola:
1. Citire lista numere intregi
2. Secventa maxima elemente egale (prop 5)
3. Secventa suma maxima (prop 11)
4. Iesire.

Proprietati: 5. toate egale. 11. suma max.

== Scenarii de rulare

=== Secventa elemente egale

#table(
  columns: (auto, auto, auto),
  align: left,
  stroke: 0.5pt,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [1], [Meniu afisat], [Alege citire],
  [Introduceti numere: 1 2 2 3 3 3 4], [], [Citire lista],
  [1], [Secventa egala: [3, 3, 3]], [Afisare rezultat],
)

Alt scenariu:

#table(
  columns: (auto, auto, auto),
  align: left,
  stroke: 0.5pt,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [1], [Meniu], [Citire],
  [5 5 5 6 7], [], [Lista],
  [1], [Secventa egala: [5, 5, 5]], [Rezultat],
)

=== Secventa suma maxima

#table(
  columns: (auto, auto, auto),
  align: left,
  stroke: 0.5pt,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [2], [Meniu], [Alege suma max],
  [1 -2 3 4 -1 2], [], [Citire],
  [2], [Secventa suma maxima: [3, 4, -1, 2]], [Afisare],
)

Altul:

#table(
  columns: (auto, auto, auto),
  align: left,
  stroke: 0.5pt,
  table.header[*Utilizator*][*Program*][*Descriere*],
  [-3 -1 -2], [], [Lista negativa],
  [2], [Secventa suma maxima: [-1]], [Rezultat],
)

== Cazuri de testare

=== Elemente egale

#table(
  columns: (auto, auto),
  align: left,
  stroke: 0.5pt,
  table.header[*Input*][*Output asteptat*],
  [1 1 2 2 2 3], [[2, 2, 2]],
  [5 5 5 5], [[5, 5, 5, 5]],
  [1 2 3 4], [[1]],
  [], [[]],
)

=== Suma maxima

#table(
  columns: (auto, auto),
  align: left,
  stroke: 0.5pt,
  table.header[*Input*][*Output asteptat*],
  [1 -2 3 5 -1 2], [[3, 5, -1, 2]],
  [-3 -1 -2], [[-1]],
  [2 4 -1 2 -1], [[2, 4, -1, 2]],
  [], [[]],
)