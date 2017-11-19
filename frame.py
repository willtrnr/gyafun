import opcodes

class Frame:
    def __init__(self, code, pc=0, operands=None, slots=None):
        self._code = code
        self._pc = pc
        self._next_pc = pc
        self._operands = operands or list()
        self._slots = slots or list()

    def __repr__(self):
        return 'Frame(code={}, pc={}, next_pc={}, operands={}, slots={})'.format(repr(self._code), repr(self._pc), repr(self._next_pc), repr(self._operands), repr(self._slots))

    def __str__(self):
        pc = self.get_pc()
        line = self.get_line_number()
        code = self.get_code()
        inst = self.get_opcode_name()
        operands = '\n    '.join(str(i) + ': ' + repr(self._operands[i]) for i in range(len(self._operands)))
        slots = '\n    '.join(str(i) + ': ' + repr(self._slots[i]) for i in range(len(self._slots)))
        return 'Frame:\n  symbol: {}\n  pc: {}\n  op: {} [{}]\n  line: {}\n  operands:\n    {}\n  slots:\n    {}'.format(self._code[0], pc, inst, repr(code[pc:pc + 7]), line or '?', operands, slots)

    def get_code(self):
        return self._code[1]

    def set_pc(self, pc):
        self._pc = pc

    def get_pc(self):
        return self._pc

    def set_next_pc(self, pc):
        self._next_pc = pc

    def get_next_pc(self):
        return self._next_pc

    def get_opcode(self):
        pc = self.get_pc()
        code = self.get_code()
        if pc < len(code):
            return code[pc]
        else:
            return None

    def get_args(self, count):
        pc = self.get_pc()
        code = self.get_code()
        return [int.from_bytes(code[pc + 1 + x * 2:pc + 1 + (x + 1) * 2], byteorder='little', signed=False) for x in range(count)]

    def push_operand(self, value):
        self._operands.append(value)

    def pop_operand(self):
        return self._operands.pop()

    def set_slot(self, idx, value):
        if idx >= len(self._slots):
            for x in range(idx - len(self._slots) + 1):
                self._slots.append(None)
        self._slots[idx] = value

    def get_slot(self, idx):
        return self._slots[idx]

    def get_opcode_name(self):
        op = self.get_opcode()
        if op is not None:
            for o in dir(opcodes):
                if o.startswith('OP_') and opcodes.__dict__[o] == op:
                    return o[3:]
        return op

    def get_line_number(self):
        return self._code[2].get(self._pc)
