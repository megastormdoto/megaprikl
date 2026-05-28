"""Simple register allocator for x86-64 code generation."""

from .abi import ABIConstants

class RegisterAllocator:
    """Manages register allocation for temporaries."""
    
    def __init__(self):
        self.available = ABIConstants.CALLER_SAVED.copy()
        self.mapping = {}  # temp -> register
        self.spill_offset = 0
    
    def alloc(self, temp_name: str) -> str:
        """Allocate a register for a temporary."""
        if not self.available:
            # No registers available, need to spill
            return self._spill(temp_name)
        reg = self.available.pop(0)
        self.mapping[temp_name] = reg
        return reg
    
    def free(self, temp_name: str):
        """Free a register that held a temporary."""
        if temp_name in self.mapping:
            reg = self.mapping.pop(temp_name)
            if reg not in self.available:
                self.available.append(reg)
    
    def _spill(self, temp_name: str) -> str:
        """Spill a temporary to stack (stub)."""
        # For now, return a stack slot
        self.spill_offset += 8
        return f"qword [rbp-{self.spill_offset}]"
