; Scrieți un program în limbaj de asamblare care să rezolve expresia aritmetică, considerând domeniile de definiție ale variabilelor
; a - doubleword; b, d - byte; c - word; e - qword
; a + b / c - d * 2 - e

bits 32

global start 

extern exit
import exit msvcrt.dll

; data segment
segment data use32 class=data
    ; a,b,c,d
    a dd 125
    b db 2
    c dw 15
    d db 200
    e dq 80
    
    
    
segment code use32 class=data
    ;
    start:
        ; b/c
        mov al, [b]
        mov ah, 0
        mov dx, 0
        ; acum, dx:ax = b
        div word [c] ; impartim doubleword-ul dx:ax la word-ul c
        ; acum, catul impartirii este in ax (restul este in dx, dar mergem mai departe doar cu catul)
        
        ; d*2
        mov bx, ax ; eliberam ax pentru inmultire, punem pe b/c in bx
        mov al, 2
        mul byte [d] ; ax=d*2
        
        
        ; (b/c) - (d*2) === bx - ax
        sub bx, ax ; bx = (b/c) - (d*2)
        
        ; a + b/c - d*2 === [a] + bx
        ; a - doubleword, deci trebuie sa convertim bx in doubleword => cx:bx
        mov cx, 0
        
        ; punem pe a in 2 registri de tip word: dx:ax = [a]
        mov ax, word [a]
        mov dx, word [a+2]
        
        add ax, bx
        add dx, cx ; dx:ax = a+ b/c + d*2
        
        ; dx:ax - [e]
        
        ; convertim dx:ax intr-un word folosind stiva
        push dx
        push ax
        pop eax
        ; transformam eax intr-un quad
        mov edx, 0 ; edx:eax = a + b / c - d * 2
        ; efectuam -e
        sub eax, dword [e]
        sbb edx, dword [e+4]
        
        ; exit(0)
        push 0
        call [exit]
       