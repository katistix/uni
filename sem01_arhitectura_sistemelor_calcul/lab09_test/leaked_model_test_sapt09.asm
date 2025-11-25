; Se da in data segment un sir de exact 10 caractere.
; Sa se citeasca un numar natural n reprezentat pe un octet (daca se introduce o valoare mai mare programul va afisa un mesaj corespunzator si se va opri din executie).
; Se cere sa se creeze n fisiere, fiecare avand numele output-i.txt, unde i=1,n. Sa se scrie in fiecare fisier primele (i+1) caractere din sirul dat (sau maxim 10 daca n>=10).
; Exemplu:
; sir: abcdefghij nume: input.txt n: 2 => output-O.txt a output-1.txt ab output-
; 2.txt abc

bits 32

global start        


extern exit, printf, scanf, fopen, fread, fclose, fprintf, sprintf, fscanf
import exit msvcrt.dll 
import printf msvcrt.dll   
import scanf msvcrt.dll
import fopen msvcrt.dll  
import fread msvcrt.dll
import fclose msvcrt.dll
import fprintf msvcrt.dll
import sprintf msvcrt.dll
import fscanf msvcrt.dll


segment data use32 class=data
    sir db "abcdefghijdjsaojdsiajdaoijdsaoijdasoidjoasdj", 0
    inputpath db "input.txt", 0
    out_path_fmt db "output-%d.txt", 0
    out_path resb 30 ; output filename, rezervam 3 caractere
    outextension db ".txt", 0
    racc db "r", 0
    wacc db "w", 0
    infmt db "%d", 0
    outfmt db "%.*s", 0
    mesaj_n db "numarul n este prea mare!", 0
    fd dd -1
    current_i dd 0
    n dd 0

segment code use32 class=code
    start:
        ; deschid fisierul de input
        push dword racc
        push dword inputpath
        call [fopen]
        add esp, 4*2

        cmp eax, 0                  
        je final
        mov dword [fd], eax

        ; citeste n din input.txt
        push dword n        ; adresa unde stocam numarul
        push dword infmt ; formatul "%d"
        push dword [fd]  ; handle-ul fisierului
        call [fscanf]
        add esp, 4*3
        ; inchide fisierul de input
        push dword [fd]
        call [fclose]
        add esp, 4

        ; daca n>=256 afiseaza un mesaj ca e prea mare
        cmp dword [n], 255
        jg mesaj_n_prea_mare

        ; scrie in fisiere
        mov ecx, n
        ; Vom folosi o bucla "manuala" cu jump, nu "loop", pentru a controla contorul mai usor
        loop_fisiere:
            mov eax, [current_i]
            cmp eax, [n]
            jg final


            ; formeaza un nou numar folosind cifrele lui i
            ; sprintf(out_name, "output-%d.txt", current_i)
            push dword [current_i]
            push dword out_path_fmt
            push dword out_path
            call [sprintf]
            add esp, 4*3

            ; deschide un fisier
            push dword wacc
            push dword out_path
            call [fopen]
            add esp, 4*2

            mov [fd], eax

            ; 3. Calculam lungimea de scriere: min(current_i + 1, 10)
            mov eax, [current_i]
            inc eax         ; Lungimea dorita este i + 1
            
            cmp eax, 10     ; Comparam cu lungimea maxima a sirului (10)
            jle lungime_ok
            mov eax, 10     ; Daca e mai mare de 10, il limitam la 10
            
            lungime_ok:
            ; In acest moment EAX contine lungimea exacta de scris

            ; scrie
            push dword sir
            push eax
            push dword outfmt
            push dword [fd]
            call [fprintf]
            add esp, 4*3

            ; incrementeaza i
            inc dword [current_i]

            ; inchide fisierul
            push dword [fd]
            call [fclose]
            add esp, 4

        jmp loop_fisiere

        jmp final
        mesaj_n_prea_mare:
            push dword mesaj_n
            call [printf]
            add esp, 4

        final:
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
