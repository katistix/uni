;Se da un sir de caractere format din litere mici.
;Sa se transforme acest sir in sirul literelor mari corespunzator.

bits 32

global start        


extern exit              
import exit msvcrt.dll    

segment data use32 class=data
    s db 'a', 'b', 'c', 'm','n'
    l equ $-s ; lungimea lui s
    d times l db 0 ; rezervarea unui spatiu de dimensiune l pentru sirul destinatie d si initializarea acestuia
    
    

segment code use32 class=code
    start:
        mov ecx, l ;punem lungimea in ECX pentru a putea realiza bucla loop de ecx ori
        mov esi, 0     

        jecxz Sfarsit
        Repeta:
            mov al, [s+esi]
            ; convert lower to upper
            mov bl, 'a'-'A'
            sub al, bl             

            mov [d+esi], al 
            inc esi        
        loop Repeta
        Sfarsit:
        
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
