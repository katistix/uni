;a - byte, b - word, c - double word, d - qword - Interpretare cu semn
;c-b-(a+a)-b 

bits 32

global start        


extern exit              
import exit msvcrt.dll    

segment data use32 class=data
    a db 0x12
    b dw 0x1234
    c dd 0x1234_5678
    d dq 0x1234_5678_9abc_def0

segment code use32 class=code
    start:
        mov ebx, dword [c]
        ; mov eax, 0 ; fara semn
        mov ax, word [b]
        cwd ; extinde wordul ax in eax
        
        sub ebx, eax
        
        ;(a+a)
        
        
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
