; Sa se citeasca de la tastatura un numar in baza 10 si sa
; se afiseze valoarea acelui numar in baza 16

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
    fmt_out db "%x", 0
    n dd 0

segment code use32 class=code
    start:
        ; citire
        push dword n
        push dword fmt_in
        call [scanf]
        add esp, 4*2

        ; afisare
        push dword [n]
        push dword fmt_out
        call [printf]
        add esp, 4*2

    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
