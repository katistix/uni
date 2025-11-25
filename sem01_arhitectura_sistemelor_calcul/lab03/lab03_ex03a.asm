;a - byte, b - word, c - double word, d - qword - Interpretare fara semn
;(c+d)-(a+d)+b 


bits 32

global start


extern exit              
import exit msvcrt.dll    

segment data use32 class=data
    a db 0x12
    b dw 0x1234
    c dd 0x1
    d dq 0x0000_0000_ffff_ffff

segment code use32 class=code
    start:
    
    
        ; a+d
        mov eax, dword [d]
        mov edx, dword [d+4]
        
        mov ebx, 0
        mov bl, byte [a]
        
        add eax, ebx
        adc edx, 0 
        ;save for later
        push eax
        push edx
        
        
        ;c+d
        mov eax, dword [d]
        mov edx, dword [d+4]
        
        add eax, [c]
        adc edx, 0 ; edx:eax = c+d
        
        ; (c+d)-(a+d)
        pop ecx
        pop ebx ; ecx:ebx = (a+d)
        
        sub eax, ebx
        sbb edx, ecx
        
        
        ; +b
        ;; facem ecx:ebx = word[b]
        mov ecx, 0
        mov ebx, 0
        mov bx, word [b]
        
        add eax, ebx
        adc edx, 0  
        
        
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
