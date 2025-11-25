; Se da un fisier text. Fisierul contine numere (in baza 10) separate prin spatii.
; Sa se citeasca continutul acestui fisier, sa se determine minimul numerelor citite
; si sa se scrie rezultatul la sfarsitul fisierului. 

; date.txt: 
; 23 432 2

bits 32 

global start        

; declare external functions needed by our program
extern exit, printf, scanf, fopen, fread, fclose, fprintf
import exit msvcrt.dll 
import printf msvcrt.dll   
import scanf msvcrt.dll
import fopen msvcrt.dll  
import fread msvcrt.dll
import fclose msvcrt.dll
import fprintf msvcrt.dll


segment data use32 class=data
    minim dd 9999
    nume_fisier db "date.txt", 0
    mod_acces db "r", 0  
    append_acces db "a", 0       
    descriptor_fis dd -1         ; variabila in care vom salva descriptorul fisierului - necesar pentru a putea face referire la fisier
    len equ 100                  ; numarul maxim de elemente citite din fisier.                            
    text times len db 0          ; sirul in care se va citi textul din fisier  
    out_format db " %d", 0


; our code starts here
segment code use32 class=code
    start:
        ; deschidem fisierul
        push dword mod_acces     
        push dword nume_fisier
        call [fopen]
        add esp, 4*2
        mov [descriptor_fis], eax 
        cmp eax, 0
        je final 
        ; citim textul in fisierul deschis folosind functia fread
        ; eax = fread(text, 1, len, descriptor_fis) = numarul de chestii citite
        push dword [descriptor_fis]
        push dword len
        push dword 1
        push dword text        
        call [fread]
        add esp, 4*4


        ; split the text at " " and form the numbers

        ; parcurg situl text
        mov ecx, eax ; eax = numarul de bytes din fisier
        mov esi, text ; incepem de la inceputul sirului
        mov ebx, 0 ; ebi = numarul curent
        start_loop:
            ; daca byte-ul curent e cifra, o adun la numarul curent
            xor eax, eax
            lodsb
            
            ; daca e mai mic ca '0' sau mai mare ca '9'
            cmp al, '0'
            jb not_digit
            cmp al, '9'
            ja not_digit

            ; daca a ajuns aici, inseamna ca e digit, si il punem in numar
            sub al, '0' ; chat -> digit
            imul ebx, 10
            add ebx, eax
            jmp next



            not_digit:
                ; calculez noul minim din sir
                cmp ebx, dword [minim]
                jge nu_e_minim
                mov dword [minim], ebx

                nu_e_minim:
                mov ebx, 0

            next:
        loop start_loop

        ; verifica ultimul numar
        cmp ebx, dword [minim]
        jge skip_final_check
        mov dword [minim], ebx
        skip_final_check:


        ; apelam functia fclose pentru a inchide fisierul
        ; fclose(descriptor_fis)
        push dword [descriptor_fis]
        call [fclose]
        add esp, 4

        ; acum avem in [minim] valoarea minima, vom deschide din nou fisierul si vom adauga in el minimul
        ; deschidem fisierul
        push dword append_acces     
        push dword nume_fisier
        call [fopen]
        add esp, 4*2
        mov [descriptor_fis], eax 
        cmp eax, 0
        je final 

        ; scriem in fisier datele de output
        ; fprintf(descriptor, format, value)
        push dword [minim]
        push dword out_format
        push dword [descriptor_fis]
        call [fprintf]
        add esp, 4*3

        ; inchidem 
        ; fclose(descriptor_fis)
        push dword [descriptor_fis]
        call [fclose]
        add esp, 4


        
      final:
        
        ; exit(0)
        push    dword 0      
        call    [exit]       