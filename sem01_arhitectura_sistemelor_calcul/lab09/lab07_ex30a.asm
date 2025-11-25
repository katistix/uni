; Se citesc de la tastatura numere (in baza 10) pana cand se introduce cifra 0.
; Determinaţi şi afişaţi cel mai mic număr dintre cele citite. 

bits 32

global start        


extern exit, printf, scanf, fopen, fread, fclose, fprintf
import exit msvcrt.dll 
import printf msvcrt.dll   
import scanf msvcrt.dll
import fopen msvcrt.dll  
import fread msvcrt.dll
import fclose msvcrt.dll
import fprintf msvcrt.dll



segment data use32 class=data
    minim dd 99999
    num dd 0
    filename db "date.txt", 0
    mode db "r", 0
    fd dd -1
    infmt db "%d", 0
    outfmt db "Numarul minim este: %d", 0

segment code use32 class=code
    start:

        start_loop:
            ; citeste numere pana cand se citeste numarul 0
            push dword num
            push dword infmt
            call [scanf]
            add esp, 4*2

            ; daca numarul citit este 0, atunci end loop
            cmp dword [num], 0
            je end_loop

            ; daca e noul minim
            mov eax, [minim]
            cmp dword [num], eax
            jge nu_e_minim
            ; actualizare minim
            mov eax, dword [num]
            mov dword [minim], eax


        
            nu_e_minim:
                jmp start_loop
        end_loop:


        ; afisare numar minim
        push dword [minim]
        push dword outfmt
        call [printf]
        add esp, 4*2

        final:
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
