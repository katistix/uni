; a - word, b - byte, c - dword

; cerinta a)
; formarea lui c
; bitii 0-2 au valoarea 0
; bitii 3-5 au valoarea 1
; bitii 6-9 coincid cu bitii 11-14 ai lui a
; bitii 10-15 coincid cu bitii 1-6 ai lui b
; bitii 16-31 au valoarea 1

; cerinta b)
; ((a+c)/b+c)*2-a  --- interpretare fara semn

bits 32

global start

extern exit
import exit msvcrt.dll

segment data use32 class=data
    a dw 0FFh
    b db 0Fh
    c resd 1

segment code use32 class=code
    start:
        
        ; calculam pe c in ebx
        mov ebx, 0
        
        ;or ebx, ..._0011_1000b
        or ebx, 0000_0038h ; am scris masca in hex ca sa fie mai scurta
        
        ; bitii 6-9 coincid cu bitii 11-14 ai lui a
        mov eax, 0
        mov ax, word [a]
        and eax, 0111_1000_0000_0000b
        shr eax, 5
        or ebx, eax
        
        ; bitii 10-15 coincid cu bitii 1-6 ai lui b
        mov eax, 0
        mov al, byte [b]
        and eax, 0000_0000_0111_1110b
        shl eax, 9
        or ebx, eax
        
        ; bitii 16-31 au valoarea 1
        or ebx, 0_FFFF_0000h
        
        
        mov dword [c], ebx
        
        

        
        
        

        

        
    
   
        