#set page(margin: 2cm)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.")

#align(center, text(16pt, weight: "bold")[Partial ALGEBRA - Varianta C])
#align(center, text(14pt, weight: "light")[varianta generata de Google Gemini])

= Problema 1

a) Să se definească următoarele noțiuni și să se dea câte un exemplu pentru fiecare: *relație de echivalență*, *element maximal* într-o mulțime ordonată, *izomorfism de grupuri*.

b) Fie $(G, dot)$ un grup și $H <= G$ un subgrup al său. Să se arate că pentru orice element fixat $g in G$, mulțimea $K = {g x g^(-1) | x in H}$ este, de asemenea, un subgrup al lui $G$ (acesta se numește subgrup conjugat).

c) Fie $f: A -> B$ o funcție cu proprietatea că $h_1 compose f = h_2 compose f => h_1 = h_2$ pentru orice mulțime $C$ și orice două funcții $h_1, h_2: B -> C$. Să se arate că $f$ este surjectivă.

= Problema 2

Se consideră funcțiile $f: RR -> RR$ și $g: RR -> [0, infinity)$, unde:

$ f(x) = cases(x - 2"," & x in (-infinity", " 3], 2x - 5"," & x in (3", " infinity)) $

și $g(x) = (x-1)^2$.

a) Să se verifice dacă funcția $f$ este injectivă și/sau surjectivă.

b) Dacă există, să se determine funcția inversă $f^(-1)$.

c) Să se determine funcția compusă $g compose f$.

d) Să se găsească două submulțimi $A, B subset.eq RR$ pentru care $f(A inter B) = f(A) inter f(B)$ (Indiciu: verifică dacă egalitatea are legătură cu injectivitatea demonstrată la punctul a).

= Problema 3

a) Să se arate că relația $(CC, CC, tilde)$ dată prin:
$ forall z, w in CC, space z tilde w <=> |z| = |w| $
este o relație de echivalență (unde $|z|$ este modulul numărului complex).

b) Să se determine mulțimea factor $CC / tilde$ și să se descrie geometric o clasă de echivalență oarecare.

c) Pe mulțimea $A = {2, 3, 4, 5, 6, 10, 12, 15}$ considerăm relația de divizibilitate $x | y$. Să se arate că este o relație de ordine. Desenați diagrama Hasse și precizați dacă există elemente incomparabile în mulțimea ordonată $(A, |)$.

= Problema 4

a) Să se arate că legea de compoziție:
$ x * y = x y - 4x - 4y + 20 $
definește o structură de grup abelian pe mulțimea $G = (4, infinity)$.

b) Să se determine un izomorfism $f: (RR^*_+, dot) -> (G, *)$ de forma $f(x) = x + a$.

c) Fie $(G, dot)$ un grup. Să se arate că dacă $(x y)^2 = x^2 y^2$ pentru orice $x, y in G$, atunci grupul $G$ este comutativ (abelian).

#line(length: 100%)

== 💡 Mentor's Commentary (Analiza subiectului)

Ca "senior", hai să îți explic de ce am ales problemele astea și unde sunt capcanele, ca să înțelegi *esența* din spatele lor:

=== La Problema 1 (Teorie Conceptuală)

- *1c)* este duala problemei din Varianta A. Acolo ți se cerea să arăți că simplificarea la stânga implică injectivitate. Aici, simplificarea la dreapta ($h_1 compose f = h_2 compose f => h_1=h_2$) implică *surjectivitate*.

  _Intuiția:_ Dacă $f$ nu atinge un punct $y in B$, pot defini două funcții $h_1, h_2$ care sunt identice peste tot, dar diferă fix în punctul $y$ "neatins". Deoarece $f$ nu ajunge niciodată în $y$, compunerea nu va "vedea" diferența, dar funcțiile sunt distincte. Asta e contradicția.

=== La Problema 2 (Funcții)

- Capcana la *2a)* este punctul de lipire $x=3$. Trebuie să verifici continuitatea și monotonia.

  Calcul: $3-2=1$ și $2(3)-5=1$. Funcția se "lipește" perfect și pantele sunt pozitive (1 și 2). Deci e strict crescătoare $->$ injectivă.

- La *2d)*, ține minte o teoremă fundamentală: Egalitatea $f(A inter B) = f(A) inter f(B)$ are loc pentru *orice* mulțimi $A, B$ *dacă și numai dacă* $f$ este injectivă. Cum la a) probabil ai demonstrat că e injectivă, poți alege ORICE mulțimi disjuncte sau care se intersectează, egalitatea va ține.

=== La Problema 3 (Relații)

- *3a) și 3b):* Relația $|z| = |w|$ înseamnă că numerele sunt la aceeași distanță de origine.

  _Geometric:_ Clasele de echivalență sunt *cercuri concentrice* cu centrul în origine. Mulțimea factor este mulțimea tuturor acestor cercuri (practic, raza $r in [0, infinity)$ indexează clasele).

- *3c):* Diagrama Hasse e cheia aici. Vei vedea că 2 divide 6 și 3 divide 6, dar 2 și 3 nu se divid între ele. Acelea sunt *elemente incomparabile*. E crucial să înțelegi că într-o relație de ordine parțială (nu totală), nu orice două elemente pot fi comparate.

=== La Problema 4 (Grupuri)

- Forma $x y - 4x - 4y + 20$ este de fapt o "translație" a înmulțirii.

  _Truc:_ Scrie sub forma canonică: $(x-4)(y-4) + 4$. Vezi cum seamănă cu $(x-a)(y-a)+a$?

  Asta îți spune imediat că elementul neutru nu e 1, ci $4+1=5$. Iar izomorfismul de la punctul b) va fi $f(x) = x+4$, care "mută" înmulțirea normală din $RR$ cu 4 unități la dreapta.
