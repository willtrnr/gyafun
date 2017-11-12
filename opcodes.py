# GYAFUN VM Op Codes

# General ops
OP_NOP = 0x00 # No-op

# Frame control
OP_RET = 0x01 # Pop the stack (if possible) and return value to previous frame

# Stack management
OP_LD0 = 0x02 # Push 0 on the stack
OP_LD1 = 0x03 # Push 1 on the stack
OP_LDC = 0x04 # Load constant from pool
OP_LDL = 0x05 # Load local from slots
OP_ST0 = 0x06 # Store 0 in local slot
OP_ST1 = 0x07 # Store 1 in local slot
OP_STC = 0x08 # Store constant from pool in local slot
OP_STL = 0x09 # Pop stack and set value in local slot
OP_POP = 0x0A # Pop and discard
OP_DUP = 0x0B # Pop stack and push the value twice

# Bitwise
OP_BND = 0x0C # &
OP_BOR = 0x0D # |
OP_BXR = 0x0E # ^
OP_BNT = 0x0F # ~
OP_BLS = 0x10 # Left shift
OP_BRS = 0x11 # Right shift

# Arithmetics
OP_ADD = 0x12 # Pop 2 values and push sum
OP_SUB = 0x13 # Pop 2 values and push difference
OP_MUL = 0x14 # Pop 2 values and push product
OP_DIV = 0x15 # Pop 2 values and push quotient
OP_MOD = 0x16 # Pop 2 values and push remainder
OP_NEG = 0x17 # Pop value and push negation
OP_CMP = 0x18 # Pop 2 values and push 0 is equal, 1 if greater and -1 otherwise

# Jumps
OP_JMP = 0x19 # Jump to instruction
OP_IVK = 0x1A # Pop n values and invoke subroutine setting up a new stack frame with popped values as locals

# Branching
OP_IZR = 0x1B # Pop value and if equal to 0 jump to address
OP_INZ = 0x1C # Pop value and if not equal to 0 jump to address
OP_IEQ = 0x1D # Pop 2 values and if equal jump to program address
OP_INE = 0x1E # Pop 2 values and if not equal jump to program address
OP_ILT = 0x1F # Pop 2 values and if first is less then second jump to program address
OP_IGT = 0x20 # Pop 2 values and if first is greater then second jump to program address
OP_IIN = 0x21 # Pop 1 value and if null jump to program address
OP_INN = 0x22 # pop 1 value and if not null jump to program address
