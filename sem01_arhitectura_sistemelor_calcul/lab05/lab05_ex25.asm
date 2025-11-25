; Se dau doua siruri de caractere S1 si S2. Sa se construiasca sirul D ce contine toate elementele din S1 care nu apar in S2. 

bits 32

global start        


extern exit              
import exit msvcrt.dll    

segment data use32 class=data
    s1 db '+', '4', '2', 'a', '8', '4', 'X', '5'
    l1 equ $-s1
    s2 db 'a', '4', '5'
    l2 equ $-s2
    
    d times l1 db 0

segment code use32 class=code
    start:
        mov ecx, l1
        mov esi, s1
        mov edi, d
        
    bucla_exterioara:
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
