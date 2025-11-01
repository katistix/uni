;Se dau cuvintele A si B. Sa se obtina dublucuvantul C:
 ;  bitii 0-4 ai lui C coincid cu bitii 11-15 ai lui A
 ;  bitii 5-11 ai lui C au valoarea 1
 ;  bitii 12-15 ai lui C coincid cu bitii 8-11 ai lui B
 ;  bitii 16-31 ai lui C coincid cu bitii lui A
bits 32

global start        


extern exit              
import exit msvcrt.dll

segment data use32 class=data
    a dw 0111011101010111b
    b dw 1001101110111110b
    c dd 0

segment code use32 class=code
    start:
        ; a 11-15 -> bx 0-4
        xor eax,eax ; zero eax
        mov ax, word [a]
        and eax, 1111100000000000b
        ror eax, 11
        or ebx, eax ;; put this part into the result
        
        ;...
        
        
        ; put final result in memory
        mov dword [c], ebx
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
