

bits 32

global start

extern exit
import exit msvcrt.dll

segment data use32 class=data
    a db 5
    b dw 1
    c dd 1
    d dq 45
    
    ad resq 1 ; to store a+d?


; c-(a+d)+(b+d)
segment code use32 class=code
    start:
        ;a+d
        mov ebx, 0
        mov ecx, 0
        mov bl, [a]
        
        mov eax, [d]
        mov edx, [d+4]
        
        add eax, ebx
        add edx, ecx ; edx:eax = a+d
        
        
        push 0
        call [exit]