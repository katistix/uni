bits 32 ; assembling for the 32 bits architecture

; declare the EntryPoint (a label defining the very first instruction of the program)
global start        

; declare external functions needed by our program
extern exit               ; tell nasm that exit exists even if we won't be defining it
import exit msvcrt.dll    ; exit is a function that ends the calling process. It is defined in msvcrt.dll
segment data use32 class=data
    ; ...


; 256/1
segment code use32 class=code
    start:
        mov ax, 255    ; put 256 into AX
        mov dx, 0      ; clear DX so dividend = 0x00000100
        mov bx, 1      ; divisor = 1
        div bx         ; unsigned divide DX:AX by BX

    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
