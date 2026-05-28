"""System V AMD64 ABI constants for x86-64 code generation."""

class ABIConstants:
    # Integer argument registers (first 6 args)
    INT_ARG_REGS = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']
    
    # Integer return register
    INT_RET_REG = 'rax'
    
    # Caller-saved registers (can be clobbered by called function)
    CALLER_SAVED = ['rax', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11']
    
    # Callee-saved registers (must be preserved by called function)
    CALLEE_SAVED = ['rbx', 'rbp', 'r12', 'r13', 'r14', 'r15']
    
    # Stack alignment requirement (16 bytes)
    STACK_ALIGNMENT = 16
    
    # Red zone size (128 bytes below rsp)
    RED_ZONE_SIZE = 128
    
    # Syscall numbers (Linux x86-64)
    SYS_EXIT = 60
    SYS_WRITE = 1
    SYS_READ = 0
