; Se da un sir de octeti S de lungime l. Sa se construiasca sirul D de lungime l-1 astfel incat elementele din D sa reprezinte produsul dintre fiecare 2 elemente consecutive S(i) si S(i+1) din S. 

bits 32

global start        


extern exit              
import exit msvcrt.dll    

segment data use32 class=data
    s db 3, 4, 5, 6
    l equ $-s
    d times l-1 db 0

segment code use32 class=code
    start:
    
        mov ecx, l-1
        mov esi, 0 ; indicele curent
        
        ; loop-ul
        jecxz sf
        Repeta:
            mov al, [s+esi]
            mul byte [s+esi+1]
            
            mov [d+esi], al
            
            inc esi
        loop Repeta
        
        sf:
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
