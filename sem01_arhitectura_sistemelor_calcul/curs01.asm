bits 32

global start        


extern exit              
import exit msvcrt.dll    

segment data use32 class=data
    a dd 12345678h, 23456789h

segment code use32 class=code
    start:
        mov ax, [a+3]
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
