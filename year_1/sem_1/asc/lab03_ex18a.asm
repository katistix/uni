;a - byte, b - word, c - double word, d - qword - Interpretare fara semn
; (d+d)-a-b-c 


bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
                          ; msvcrt.dll contains exit, printf and all the other important C-runtime specific functions

; our data is declared here (the variables needed by our program)
segment data use32 class=data
    ; ...
    a db 12
    b dw 23
    c dd 32
    d dq 43

; our code starts here
segment code use32 class=code
    start:
        ; edx:eax 
        ; const(0):ecx
        ; d+d
        
        ;; edx:eax = d+d
        ; eax - low bits
        mov eax, dword [d]
        add eax, dword [d]
        ; edx - high bits
        mov edx, dword [d+4]
        adc edx, dword [d+4]
        
        ; - a
        ;; transformam [a]
        mov ecx, 0
        mov cl, byte [a] ; converted [a] to a dword
        
        sub eax, ecx
        sbb edx, 0x00
        
        ; -b
        mov ecx, 0
        mov cx, word [b]
        
        sub eax, ecx
        sbb edx, 0x00
        
        ; -c
        mov ecx, dword [c]
        
        sub eax, ecx
        sbb edx, 0x00
        
        
    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
