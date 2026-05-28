; Runtime library for MiniCompiler
; Linux x86-64, NASM syntax

section .text
global _start
global exit
global print_int
global print_string

; Program entry point
_start:
    call main
    mov rdi, rax
    mov rax, 60         ; syscall: exit
    syscall

; exit(rdi) - exit with status code
exit:
    mov rax, 60
    syscall

; print_int(rdi) - print integer to stdout
print_int:
    ; Stub: just return for now
    ret

; print_string(rdi) - print null-terminated string to stdout
print_string:
    ; Stub: just return for now
    ret
