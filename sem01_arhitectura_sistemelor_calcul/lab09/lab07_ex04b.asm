; NOT WORKING

; 04b. Se da un fisier text. Sa se citeasca continutul fisierului,
; sa se contorizeze numarul de cifre impare si sa se afiseze aceasta valoare.
; Numele fisierului text este definit in segmentul de date. 

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
    infile db "input.txt", 0
    racc db "r", 0
    fd dd -1

    outfmt db "%d", 0

    len equ 100                  ; numarul maxim de elemente citite din fisier.                            
    buffer times len db 0          ; sirul in care se va citi textul din fisier  

    

segment code use32 class=code
    start:

        ; deschid fisierul
        push dword racc
        push dword infile
        call [fopen]
        add esp, 4*2
        cmp eax, 0
        je final
        mov dword [fd], eax

        ; citesc fisierul si il bag intr-un buffer
        push dword [fd]
        push dword len
        push dword 1
        push dword buffer
        call [fread]
        add esp, 4*4

        ; inchidem fisierul
        push dword [fd]
        call [fclose]
        add esp, 4

        mov ecx, 0

        ; parcurgem fiecare caracter si daca este cifra impara crestem contorul ecx
        mov esi, buffer
        parcurge_sir:
            lodsb                       ; load byte from intext into AL
            test    al, al             ; check for null terminator
            jz      final_parcurge_sir     ; if null terminator, we're done

            ; transforma caracterul in numar
            sub al, '0'

            ; verifica daca e impar
            test al, 1
            jz e_par
            inc ecx ; daca e impar crestem contorul

            e_par:
            

        jmp parcurge_sir
        final_parcurge_sir:

        ; scrie numarul de cifre impare
        ; printf(format, values)
        push dword [ecx]
        push dword outfmt
        call [printf]
        add esp, 4*2

        final:
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
