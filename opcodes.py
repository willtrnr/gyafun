# GYAFUN VM Op Codes

# General ops
OP_NOP = 0x00 # No-op

# Frame control
OP_RET = 0x01 # Pop the stack and return value to previous frame

# Stack management
OP_LD0 = 0x02 # Push 0 on the stack
OP_LD1 = 0x03 # Push 1 on the stack
OP_LDN = 0x04 # Push null on the stack
OP_LDC = 0x05 # Load constant from pool
OP_LDL = 0x06 # Load local from slots
OP_ST0 = 0x07 # Store 0 in local slot
OP_ST1 = 0x08 # Store 1 in local slot
OP_STN = 0x09 # Store null in local slot
OP_STC = 0x0A # Store constant from pool in local slot
OP_STL = 0x0B # Pop stack and set value in local slot
OP_POP = 0x0C # Pop and discard
OP_DUP = 0x0D # Pop stack and push the value twice
OP_SWP = 0x0E # Pop 2 values and push in reverse order

# Arrays
OP_ANW = 0x0F # Pop value and make new array of value length
OP_ASZ = 0x10 # Pop value as array and push size of array
OP_ALD = 0x11 # Pop 2 values for array and index and push value at index
OP_AST = 0x12 # Pop 3 value for array, index and value and set value at index
OP_APS = 0x13 # Pop 2 value for array and value then push value at end of array
OP_APO = 0x14 # Pop value as array and remove last value pushing it back

# Maps
OP_MNW = 0x15 # Push new map
OP_MSZ = 0x16 # Pop value as map and push count of keys
OP_MLD = 0x17 # Pop 2 values for map and key and push value at key
OP_MST = 0x18 # Pop 3 values for map, key and value and store in map
OP_MRM = 0x19 # Pop 2 values for map and key and remove from map
OP_MCT = 0x1A # Pop 2 values for map and key and push whether key is in map

# Bitwise
OP_BND = 0x1B # Pop 2 values and &
OP_BOR = 0x1C # Pop 2 values and |
OP_BXR = 0x1D # Pop 2 values and ^
OP_BNT = 0x1E # Pop 2 values and ~
# FIXME these two should accept the shift by stack and not by argument
OP_BLS = 0x1F # Pop value and left shift by n
OP_BRS = 0x20 # Pop value and right shift by n

# Arithmetics
OP_ADD = 0x21 # Pop 2 values and push sum
OP_SUB = 0x22 # Pop 2 values and push difference
OP_MUL = 0x23 # Pop 2 values and push product
OP_DIV = 0x24 # Pop 2 values and push quotient
OP_MOD = 0x25 # Pop 2 values and push remainder
OP_NEG = 0x26 # Pop value and push negation
OP_INC = 0x27 # Pop value, increment by n and push result
OP_DEC = 0x28 # Pop value, decrement by n and push result

# Jumps
OP_JMP = 0x29 # Jump to instruction
OP_IVK = 0x2A # Pop n values and invoke subroutine setting up a new stack frame with popped values as locals

# Branching
OP_IZR = 0x2B # Pop value and if equal to 0 jump to address
OP_INZ = 0x2C # Pop value and if not equal to 0 jump to address
OP_IEQ = 0x2D # Pop 2 values and if equal jump to program address
OP_INE = 0x2E # Pop 2 values and if not equal jump to program address
OP_ILT = 0x2F # Pop 2 values and if first is less then second jump to program address
OP_ILE = 0x30 # Pop 2 values and if first is less or equal then second jump to program address
OP_IGT = 0x31 # Pop 2 values and if first is greater then second jump to program address
OP_IGE = 0x32 # Pop 2 values and if first is greater or equal second the jump to program address
OP_IIN = 0x33 # Pop 1 value and if null jump to program address
OP_INN = 0x34 # Pop 1 value and if not null jump to program address

# Debug
OP_TRB = 0xCC # Start verbose mode
OP_TRS = 0xDD # Stop verbose mode
OP_BRK = 0xBB # Stop execution, display frame information and wait for continue
