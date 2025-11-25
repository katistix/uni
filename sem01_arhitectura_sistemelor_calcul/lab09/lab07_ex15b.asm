; Se dau un nume de fisier si un text (definite in segmentul de date).
; Textul contine litere mici, litere mari, cifre si caractere speciale.
; Sa se inlocuiasca toate caracterele speciale din textul dat cu caracterul 'X'.
; Sa se creeze un fisier cu numele dat si sa se scrie textul obtinut in fisier. 

bits 32

global start        


extern exit, printf, scanf, fopen, fread, fclose, fprintf, sprintf, fscanf
import exit msvcrt.dll 
import printf msvcrt.dll   
import scanf msvcrt.dll
import fopen msvcrt.dll  
import fread msvcrt.dll
import fclose msvcrt.dll
import fprintf msvcrt.dll
import sprintf msvcrt.dll
import fscanf msvcrt.dll



segment data use32 class=data
    wmode db "w", 0
    fd dd -1
    filename db "out_file.txt", 0
    intext db "abc ! def $ ghi ,", 0
    outtext resb 100
    special_chars db "!$#@,. ", 0

segment code use32 class=code
    start:

        ; Copy intext to outtext while replacing special characters with 'X'
        mov     esi, intext        ; source pointer
        mov     edi, outtext       ; destination pointer
    replace_loop:
        lodsb                       ; load byte from intext into AL

        ; make sure we are not at the end of the string
        test    al, al             ; check for null terminator
        jz      done_replacing     ; if null terminator, we're done


        ; we now check if AL is a special character (by comparing with each in special_chars)
        mov    ebx, special_chars ; pointer to special characters
        check_special:
            mov     cl, [ebx]          ; load special character
            ; check if end of special_chars
            test    cl, cl             
            jz      end_special_check        

            cmp     al, cl             ; compare current char with special char
            je      is_special         ; if equal, it's a special character
            inc     ebx                ; move to next special character
        jmp     check_special
        
        is_special:
            mov     al, 'X'           ; replace with 'X'
        end_special_check:


        ; store AL (modified or not) into outtext
        stosb                       ; store byte in outtext

    jmp replace_loop

    done_replacing:
        mov     byte [edi], 0      ; null-terminate outtext string


    ; Create and write to the file
    ; open a file in write mode
        push    dword wmode        ; push mode "w"
        push    dword filename     ; push filename
        call    [fopen]            ; call fopen
        add     esp, 4*2           ; clean up the stack
        mov     [fd], eax          ; store file descriptor

        ; write outtext to the file
        push    dword outtext      ; push the text to write
        push    dword [fd]         ; push the file descriptor
        call    [fprintf]          ; call fprintf
        add     esp, 4*2           ; clean up the stack

        ; close the file
        push    dword [fd]         ; push the file descriptor
        call    [fclose]           ; call fclose
        add     esp, 4             ; clean up the stack

    
        ; exit(0)
        push    dword 0      ; push the parameter for exit onto the stack
        call    [exit]       ; call exit to terminate the program
