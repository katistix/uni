; Se da un nume de fisier (definit in segmentul de date).
; Sa se creeze un fisier cu numele dat,
; apoi sa se citeasca de la tastatura cuvinte pana cand se citeste de la tastatura caracterul '$'.
; Sa se scrie in fisier doar cuvintele care contin cel putin o litera mare (uppercase). 

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
    out_file db "output.txt", 0
    wmode db "w", 0
    fd dd -1
    fmt_in db "%s", 0


    buffer resb 100 ; cuvantul citit
    dollar db "$", 0

segment code use32 class=code
    start:

        ; deschide fisierul pentru scriere
        push dword wmode
        push dword out_file
        call [fopen]
        add esp, 4*2
        mov [fd], eax

    read_loop:
        ; citeste un cuvant de la tastatura
        push dword buffer
        push dword fmt_in
        call [scanf]
        add esp, 4*2

        ; verifica daca cuvantul este '$'
        push dword buffer
        push dword dollar
        call [strcmp]
        add esp, 4*2
        cmp eax, 0

        je done_reading ; daca este '$', iesi din bucla

        ; verifica daca cuvantul contine cel putin o litera mare
        mov esi, buffer
        mov ecx, 0 ; flag pentru litera mare gasita
    check_uppercase:
        mov al, [esi]
        test al, al
        jz check_done ; daca am ajuns la sfarsitul cuvantului, iesim
        cmp al, 'A'
        jl not_uppercase
        cmp al, 'Z'
        jg not_uppercase
        mov ecx, 1 ; am gasit o litera mare
        jmp check_done
    not_uppercase:
        inc esi
        jmp check_uppercase
    check_done:
        cmp ecx, 0
        je read_loop ; daca nu am gasit litera mare, citeste urmatorul cuvant

        ; scrie cuvantul in fisier
        push dword buffer
        push dword [fd]
        call [fprintf]
        add esp, 4*2


        done_reading:

        ; inchide fisierul
        push dword [fd]
        call [fclose]
        add esp, 4*1
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
