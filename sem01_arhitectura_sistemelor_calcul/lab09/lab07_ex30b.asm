; Se da un nume de fisier (definit in segmentul de date).
; Sa se creeze un fisier cu numele dat,
; apoi sa se citeasca de la tastatura cuvinte pana cand
; se citeste de la tastatura caracterul '$'.
; Sa se scrie in fisier doar cuvintele care contin cel putin o cifra. 

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
    outfile db "output.txt", 0
    dollar db "$", 0
    in_fmt db "%s", 0
    outfmt db "%s ", 0
    wacc db "w", 0
    fd dd -1
    buffer resb 100


segment code use32 class=code
    start:
        ; open file
        push dword wacc
        push dword outfile
        call [fopen]
        add esp, 4*2
        mov [fd], eax 
        ; error handling meh
        test eax,eax
        jz final

        input_loop:
            ; citeste input
            push dword buffer
            push dword in_fmt
            call [scanf]
            add esp, 4*2

            ; daca end of input
            push dword buffer
            push dword dollar
            call [strcmp]
            cmp eax, 0
            je final_input ; daca s-a gasit "$"

            ; parcurgem cuvantul si il afisam doar daca are cifre
            mov esi, buffer
            mov ecx, 0 ; flag pentru litera mare gasita


            parcurge_sir:
                ; daca nu s-a ajuns la finalul cuvantului
                mov al, [esi]
                test al, al
                jz check_done ; daca am ajuns la sfarsitul cuvantului, iesim
                cmp al, '0'
                jl next_char
                cmp al, '9'
                jg next_char

                ; daca am ajuns aici inseamna ca e cifra, deci marcam flag-ul
                mov ecx, 1

                next_char:
                    inc esi
                jmp parcurge_sir
            check_done:

            ; daca flag-ul este false inseamna ca nu e bun si sarim peste el
            cmp ecx, 0
            je next_word

            ; daca am ajuns aici, ecx==1 deci scriem cuvantul: fprintf(fd, buffer)
            push dword buffer
            push dword outfmt
            push dword [fd]
            call [fprintf]
            add esp, 4*2

            next_word:
            jmp input_loop

        final_input:

        ; close the file
        push dword [fd]
        call [fclose]
        add esp, 4
    
        final:
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
