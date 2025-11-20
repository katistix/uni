#set page(margin: 2cm)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.")

#align(center, text(16pt, weight: "bold")[ALGEBRA - Varianta D])
#align(center, text(12pt, style: "italic")[(Propusă pentru antrenament)])

= Problema 1 (Teorie și Structuri)

*a)* Să se definească următoarele noțiuni și să se dea câte un exemplu pentru fiecare: *Partiție a unei mulțimi*, *Nucleul unei acțiuni a unui grup pe o mulțime*, *Domeniu de integritate*.

_(Nota: Acestea sunt concepte fundamentale din curs care nu au fost cerute la definiții în variantele A-C)._

*b)* Fie $(G, dot)$ un grup. Definim *Centrul grupului* ca fiind mulțimea $Z(G) = {z in G | z g = g z, forall g in G}$. Să se arate că $Z(G)$ este un subgrup al lui $G$ și, mai mult, că este un subgrup abelian, chiar dacă $G$ nu este abelian.

*c)* Fie $f: A -> B$ o funcție. Să se arate că $f$ este injectivă dacă și numai dacă $f$ are o *inversă la stânga* (adică există $g: B -> A$ astfel încât $g compose f = 1_A$).

#line(length: 100%)

= Problema 2 (Funcții)

Se consideră funcțiile $f: RR -> RR$ și $g: RR -> RR$, definite astfel:

$ f(x) = cases(1-x"," & x in (-infinity", " 1], ln x"," & x in (1", " infinity)) $

și $g(x) = x^3 + 1$.

*a)* Să se studieze injectivitatea și surjectivitatea funcției $f$. (Atenție la grafic și monotonie!).

*b)* Să se determine imaginea funcției, $"Im" f$, și preimaginea $f^(-1)([-1, 1])$.

*c)* Să se calculeze $(g compose f)(x)$ pentru $x in RR$.

*d)* Să se demonstreze sau să se contrazică egalitatea: $f(A inter B) = f(A) inter f(B)$ pentru cazul specific al funcției $f$ de mai sus, alegând convenabil mulțimile $A$ și $B$.

#line(length: 100%)

= Problema 3 (Relații)

*a)* Pe mulțimea numerelor complexe $CC$ definim relația $tilde$ prin:
$ z tilde w <=> "Re"(z) = "Re"(w) $

Să se arate că $tilde$ este o relație de echivalență și să se descrie geometric o clasă de echivalență (ce figură geometrică reprezintă?).

*b)* Fie mulțimea $D_12 = {1, 2, 3, 4, 6, 12}$ (divizorii lui 12). Considerăm relația de divizibilitate $x | y$.

1. Să se deseneze *diagrama Hasse* a acestei mulțimi ordonate.

2. Este această structură o *latice*? Justificați calculând $2 or 3$ (supremum) și $4 and 6$ (infimum).

#line(length: 100%)

= Problema 4 (Grupuri)

Pe mulțimea $G = (3, infinity)$ se definește legea de compoziție:
$ x * y = x y - 3x - 3y + 12 $

*a)* Să se arate că $(G, *)$ este un grup abelian. Care este elementul neutru?

*b)* Să se construiască un izomorfism $f: (RR^*_+, dot) -> (G, *)$ de forma $f(x) = x + k$.

*c)* Fie $(G, dot)$ un grup oarecare. Să se arate că dacă $(x y)^(-1) = x^(-1) y^(-1)$ pentru orice $x, y in G$, atunci grupul $G$ este comutativ (abelian).

_(Indiciu: Folosiți formula uzuală a inversei produsului)_

#line(length: 100%)

== 💡 Mentor's Commentary (De ce am ales asta?)

Ca să iei nota maximă, trebuie să înțelegi capcanele din acest subiect nou:

=== La Problema 1 (Teorie)

- La punctul *b)*, Centrul grupului ($Z(G)$) este "vărul" subgrupului conjugat din Varianta C. Trebuie să verifici criteriul subgrupului: $1 in Z(G)$ (evident, neutru comută cu toți), dacă $x, y in Z(G) => x y in Z(G)$ și $x^(-1) in Z(G)$.

- La punctul *c)*, este teorema duală celei din Varianta C. Acolo simplificarea la dreapta implica surjectivitate. Aici, existența inversei la stânga implică injectivitate. Intuiția: Dacă pot "da înapoi" din $B$ în $A$ și ajung fix de unde am plecat ($x$), înseamnă că $f$ nu a "strivit" două elemente distincte $x_1 != x_2$ în același $y$, pentru că $g$ nu ar fi știut unde să-l trimită pe $y$ înapoi.

=== La Problema 2 (Funcții "Lipite")

- Funcția $f$ propusă de mine are o capcană mare. Pe $(-infinity, 1]$ este $1-x$ (descrescătoare), iar pe $(1, infinity)$ este $ln x$ (crescătoare).

- *Atenție:* Deși este continuă în 1 ($1-1=0$ și $ln 1 = 0$), faptul că descrește și apoi crește înseamnă că *NU este injectivă* (o dreaptă orizontală $y=0.5$ va tăia graficul de două ori). Asta te ajută imens la punctul *d)*, unde vei arăta că egalitatea intersecțiilor NU are loc.

=== La Problema 3 (Geometrie și Latici)

- Dacă la variantele trecute aveam $|z|=|w|$ (cercuri), $"Re"(z) = "Re"(w)$ înseamnă că numerele au aceeași parte reală. Geometric, clasele de echivalență sunt *drepte verticale* paralele cu axa imaginară.

- La subpunctul b), diagrama Hasse pentru $D_12$ este un "cub" turtit. Laticea este o structură pe care profesorii o adoră. $x or y$ este cel mai mic multiplu comun, iar $x and y$ este cel mai mare divizor comun.

=== La Problema 4 (Izomorfisme)

- Legea $x y - 3x - 3y + 12$ se restrânge canonic la $(x-3)(y-3) + 3$.

- Vezi "shift-ul"? Este cu $+3$. Deci elementul neutru va fi $3+1=4$, nu 1. Iar izomorfismul va fi $f(x) = x+3$.

- La punctul *c)*, capcana este subtilă. Formula standard într-un grup este $(x y)^(-1) = y^(-1) x^(-1)$. Dacă problema îți spune că $(x y)^(-1) = x^(-1) y^(-1)$ (adică inversa nu inversează ordinea), egalând cele două relații obții $y^(-1) x^(-1) = x^(-1) y^(-1)$. Luând inversele ambelor părți, ajungi la $x y = y x$, deci $G$ e abelian.