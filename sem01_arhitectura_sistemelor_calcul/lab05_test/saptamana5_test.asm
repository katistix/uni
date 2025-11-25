; IMPORTANT: nu mai retin daca acesta e codul initial
; sau cel pe care l-am modificat eu.


; Expresie: (a + b + d) - (a - c + d) + (b - c)
; Tipuri fara semn: a=byte, b=word, c=dword, d=qword
; Rezultat dorit pe 64 de biti in EDX:EAX
; ATENTIE: Aceasta varianta contine 12 greseli intentionate.


bits 32
global  start

extern  exit
import  exit msvcrt.dll

segment data use32 class=data
    a   db  12
    b   dw  300
    c   dd  100000
    d   dq  4000000000

    t1  dq  0
    t2  dq  0
    t3  dq  0
    tres dq 0

segment code use32 class=code
start:
    ; ---------------------------
    ; T1 = a + b + d
    ; ---------------------------
    movzx   eax, byte [a]      
     xor   edx, edx          
    ;mov     ebx, [b]  
    movzx ebx, word [b]
    add     eax, ebx
    ;sbb     edx, 0  
    adc edx,0

    ;add     edx, dword [d]  
    ;adc     eax, dword [d+4] 
    add     eax, dword [d]  
    adc     edx, dword [d+4]    
      
    mov     [t1],   edx      
    mov     [t1+4], eax

    ; ---------------------------
    ; T2 = a - c + d
    ; ---------------------------
    movzx   eax, byte [a]     
    ; sub     dword [c], eax 
    mov ebx, dword [c]
    sub eax, ebx
     xor   edx, edx   
     
    ;sub     eax, dword [d]    
    ;sbb     edx, dword [d+4]
    add     eax, dword [d]    
    adc     edx, dword [d+4]
    mov     [t2],   eax
    mov     [t2+4], edx

    ; ---------------------------
    ; tres = t1 - t2
    ; ---------------------------
    mov     eax, [t1]
    mov     edx, [t1+4]
    ;add     eax, [t2]        
    ;adc     edx, [t2+4] 
    sub     eax, [t2]        
    sbb     edx, [t2+4]      
    mov     [tres],   eax
    mov     [tres+4], edx

    ; ---------------------------
    ; T3 = b - c   
    ; ---------------------------
    xor     edx, edx
    movzx   eax, word [b]
    sub     eax, [c]
    sbb     edx, 0
    mov     [t3],   eax
    mov     [t3+4], edx

    ; ---------------------------
    ; Rezultat final: U = tres + t3
    ; ---------------------------
    mov     eax, [tres]
    mov     edx, [tres+4]
    add     eax, [t3]
    adc     edx, [t3+4]

    push    dword 0
    call    [exit]
