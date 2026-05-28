"""Stack frame management for x86-64 code generation."""

class StackFrameManager:
    """Manages stack frame layout and variable offsets."""
    
    def __init__(self):
        self.local_offset = 0
        self.locals = {}  # var_name -> offset
        self.total_size = 0
    
    def allocate_local(self, name: str, size: int, alignment: int = 8) -> int:
        """Allocate space for a local variable on stack."""
        # Align offset
        self.local_offset = ((self.local_offset + alignment - 1) // alignment) * alignment
        offset = -self.local_offset - size
        self.locals[name] = offset
        self.local_offset += size
        return offset
    
    def get_local_offset(self, name: str) -> int:
        """Get stack offset for a local variable."""
        return self.locals.get(name, 0)
    
    def finalize(self):
        """Calculate total stack frame size (aligned to 16 bytes)."""
        self.total_size = ((self.local_offset + 15) // 16) * 16
        return self.total_size
    
    def prologue(self, rbp_used: bool = True) -> str:
        """Generate function prologue assembly."""
        lines = []
        if rbp_used:
            lines.append("    push rbp")
            lines.append("    mov rbp, rsp")
        if self.total_size > 0:
            lines.append(f"    sub rsp, {self.total_size}")
        return "\n".join(lines) if lines else ""
    
    def epilogue(self, rbp_used: bool = True) -> str:
        """Generate function epilogue assembly."""
        lines = []
        if self.total_size > 0:
            lines.append("    mov rsp, rbp")
        if rbp_used:
            lines.append("    pop rbp")
        lines.append("    ret")
        return "\n".join(lines)
