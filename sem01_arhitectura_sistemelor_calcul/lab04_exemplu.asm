; Se dau cuvintele A si B. Se cere cuvantul C format astfel:
;- bitii 0-2 ai lui C coincid cu bitii 10-12 ai lui B
;- bitii 3-6 ai lui C au valoarea 1
;- bitii 7-10 ai lui C coincid cu bitii 1-4 ai lui A
;- bitii 11-12 ai valoarea 0
;- bitii 13-15 ai lui C concid cu inversul bitilor 9-11 ai lui B

bits 32

global start        


extern exit              
import exit msvcrt.dll    

segment data use32 class=data
    a dw 0111_0111_0101_0111b
    b dw 1001_1011_1011_1110b
    c dw 0

segment code use32 class=code
    start:
        mov bx, 0
        
        ; 10-12 B -> 0-2 C
        mov ax, word [b]
        and ax, 0001_1100_0000_0000b
        ror ax, 10
        or bx, ax
        
        or bx, 0000_0000_0111_1000b
        
        mov ax, word [a]
        and ax, 0000_0000_0001_1110b
        rol ax, 6
        or bx, ax
        
        and  bx, 1110011111111111b ; facem biti 11-12 din rezultat sa aiba valoarea 0
        
        mov ax, word [b]
        not ax ; inversam bitii
        and ax, 0000_1110_0000_0000b
        rol ax, 4
        or bx, ax
        
        
        
        ; punem rezultatul in memorie
        mov [c], bx
        
        
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
