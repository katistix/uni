; 25. Sa se citeasca de la tastatura doua numere a si b (in baza 10)
; şi să se determine relaţia de ordine dintre ele (a < b, a = b sau a > b).
; Afisati rezultatul în următorul format: "<a> < <b>, <a> = <b> sau <a> > <b>". 

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
    fmt_in db "%d", 0
    fmt_out db "%d %s %d", 0
    comp resb 1
    a resd 1
    b resd 1


segment code use32 class=code
    start:

        ; citeste a
        push dword a
        push dword fmt_in
        call [scanf]
        add esp, 4*2

        ; citeste b
        push dword b
        push dword fmt_in
        call [scanf]
        add esp, 4*2

        ; compara a si b
        mov eax, [a]
        mov ebx, [b]
        cmp eax, ebx
        jl a_less_b
        je a_equ_b
        jg a_greater_b

        a_less_b:
            mov byte [comp], '<'
            jmp final
        
        a_equ_b:
            mov byte [comp], '='
            jmp final

        a_greater_b:
            mov byte [comp], '>'
            jmp final
        
    
        final:
            ; afiseaza rezultatul
            push dword [b]
            push dword comp
            push dword [a]
            push dword fmt_out
            call [printf]
            add esp, 4*4

        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
