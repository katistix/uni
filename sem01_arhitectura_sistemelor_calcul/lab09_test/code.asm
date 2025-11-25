; Varianta 2

bits 32

global start        


extern exit, printf, scanf, fopen, fread, fclose, fprintf, sprintf, fscanf, strcmp
import exit msvcrt.dll 
import printf msvcrt.dll   
import scanf msvcrt.dll
import fopen msvcrt.dll  
import fread msvcrt.dll
import fclose msvcrt.dll
import fprintf msvcrt.dll
import sprintf msvcrt.dll
import fscanf msvcrt.dll
import strcmp msvcrt.dll



segment data use32 class=data
    fisier_in db "input.txt", 0
    racc db "r", 0

    fisier_out resb 20 
    wacc db "w", 0
    fmt_output db "%d", 10, "%s", 0
    fmt_input db "%s", 0 ; format pentru citirea numelui fisierului de iesire de la tastatura
    
    fmt_no_vowels db "nu exista", 0
    vocale_max resb 10 ; sir in care vom salva vocalele cu frecventa maxima

    fd dd -1

    frecvente db 0, 0, 0, 0, 0   ; A, E, I, O, U
    frecv_max db 0


    ; fmt_print_max db "Frecventa maxima a unei vocale este: %d", 10, 0


    len equ 100                  ; numarul maxim de elemente citite din fisier.                            
    text times len db 0          ; sirul in care se va citi textul din fisier  

segment code use32 class=code
    start:

        ; deschidem fisierul
        push dword racc     
        push dword fisier_in
        call [fopen]
        add esp, 4*2
        mov [fd], eax 
        ; daca nu se poate deschide fisierul, iesim
        cmp eax, 0
        je final

        ; citim textul in fisierul deschis folosind functia fread
        push dword [fd]
        push dword len
        push dword 1
        push dword text        
        call [fread]
        add esp, 4*4

        ; inchidem fisierul
        push dword [fd]
        call [fclose]
        add esp, 4

        ; parcurgem textul si calculam frecventele vocalelor (fie litere mici sau mari)
        mov esi, text 
        loop_text:
            lodsb ; bagam caracterul curent in AL
            ; verificam daca e sfarsit de sir
            test al, al
            jz final_loop_text


            ; verificam vocalele
            ; se putea face cu un sir de genul "AaEeIiOoUu" si un loop
            cmp al, 'A'
            je inc_a
            cmp al, 'a'
            je inc_a
            cmp al, 'E'
            je inc_e
            cmp al, 'e'
            je inc_e
            cmp al, 'I'
            je inc_i
            cmp al, 'i'
            je inc_i
            cmp al, 'O'
            je inc_o
            cmp al, 'o'
            je inc_o
            cmp al, 'U'
            je inc_u
            cmp al, 'u'
            je inc_u
            
            jmp final_check_vocala

            inc_a:
                inc byte [frecvente + 0]
                jmp final_check_vocala
            inc_e:
                inc byte [frecvente + 1]
                jmp final_check_vocala
            inc_i:
                inc byte [frecvente + 2]
                jmp final_check_vocala
            inc_o:
                inc byte [frecvente + 3]
                jmp final_check_vocala
            inc_u:
                inc byte [frecvente + 4]
                jmp final_check_vocala

            final_check_vocala:
            jmp loop_text
        final_loop_text:
        ; acum avem vectorul de frecvente complet

        ; calculam frecventa maxima
        mov esi, frecvente
        lodsb
        mov [frecv_max], al ; consideram prima valoare ca fiind maxima
        mov ecx, 4 ; mai avem de verificat inca 4 valori
        calc_frecv_max_loop:
            lodsb
            cmp al, [frecv_max]
            jle no_update_max ; daca AL <= frecv_max, nu actualizam
            mov [frecv_max], al ; daca am gasit o valoare mai mare, o salvam

            no_update_max:
        loop calc_frecv_max_loop

        ; acum avem frecventa maxima in frecv_max

        ; citeste de la tastatura numele fisierului de iesire
        push dword fisier_out
        push dword fmt_input
        call [scanf]
        add esp, 4*2

        ; verificam daca exista vocale (frecv_max > 0)
        movzx eax, byte [frecv_max]
        cmp eax, 0
        je no_vowels_found

        ; construim sirul cu vocalele care au frecventa maxima
        mov edi, vocale_max
        mov esi, frecvente
        mov bl, [frecv_max]
        
        ; verificam A
        cmp byte [esi], bl
        jne check_e
        mov al, 'a'
        stosb
        mov al, ' '
        stosb
        
        check_e:
        inc esi
        cmp byte [esi], bl
        jne check_i
        mov al, 'e'
        stosb
        mov al, ' '
        stosb
        
        check_i:
        inc esi
        cmp byte [esi], bl
        jne check_o
        mov al, 'i'
        stosb
        mov al, ' '
        stosb
        
        check_o:
        inc esi
        cmp byte [esi], bl
        jne check_u
        mov al, 'o'
        stosb
        mov al, ' '
        stosb
        
        check_u:
        inc esi
        cmp byte [esi], bl
        jne end_vowel_string
        mov al, 'u'
        stosb
        mov al, ' '
        stosb
        
        end_vowel_string:
            ; inlocuim ultimul spatiu cu null terminator
            dec edi
            mov byte [edi], 0

        ; deschidem fisierul de iesire
        push dword wacc
        push dword fisier_out
        call [fopen]
        add esp, 4*2
        mov [fd], eax

        cmp eax, 0
        je final

        ; scriem frecventa maxima si vocalele in fisierul de iesire
        movzx eax, byte [frecv_max]
        push dword vocale_max
        push eax
        push dword fmt_output
        push dword [fd]
        call [fprintf]
        add esp, 4*4

        ; inchidem fisierul
        push dword [fd]
        call [fclose]
        add esp, 4

        jmp final

        no_vowels_found:
            ; deschidem fisierul de iesire
            push dword wacc
            push dword fisier_out
            call [fopen]
            add esp, 4*2
            mov [fd], eax

            cmp eax, 0
            je final

            ; scriem "nu exista" in fisierul de iesire
            push dword fmt_no_vowels
            push dword [fd]
            call [fprintf]
            add esp, 4*2

        ; inchidem fisierul
        push dword [fd]
        call [fclose]
        add esp, 4

        
        final:
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
