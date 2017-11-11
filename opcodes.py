# GYAFUN VM Op Codes

# General ops
OP_NOP = 0x00 # No-op

# Frame control
OP_RET = 0x01 # Pop the stack (if possible) and return value to previous frame

# Memory management
OP_LDC = 0x02 # Load constant from pool
OP_LDL = 0x03 # Load local from slots
OP_STL = 0x04 # Pop stack and set value in local slot
OP_POP = 0x05 # Pop and discard
OP_DUP = 0x06 # Pop stack and push the value twice

# Bitwise
OP_BND = 0x07 # &
OP_BOR = 0x08 # |
OP_BXR = 0x09 # ^
OP_BNT = 0x0A # ~
OP_BLS = 0x0B # Left shift
OP_BRS = 0x0C # Right shift

# Arithmetics
OP_ADD = 0x0D # Pop 2 values and push sum
OP_SUB = 0x0E # Pop 2 values and push difference
OP_MUL = 0x0F # Pop 2 values and push product
OP_DIV = 0x10 # Pop 2 values and push quotient
OP_MOD = 0x11 # Pop 2 values and push remainder
OP_NEG = 0x12 # Pop value and push negation

# Jumps
OP_JMP = 0x13 # Jump to instruction
OP_IVK = 0x14 # Pop n values and invoke subroutine setting up a new stack frame with popped values as locals
OP_IEQ = 0x15 # Pop 2 values and if equal jump to program address
OP_INE = 0x16 # Pop 2 values and if not equal jump to program address
OP_ILT = 0x17 # Pop 2 values and if first is less then second jump to program address
OP_IGT = 0x18 # Pop 2 values and if first is greater then second jump to program address
OP_IIN = 0x19 # Pop 1 value and if null jump to program address
OP_INN = 0x1A # pop 1 value and if not null jump to program address
