import opcodes

class Frame:
    def __init__(self, code, pc=0, operands=None, slots=None):
        self._code = code
        self._pc = pc
        self._operands = operands or list()
        self._slots = slots or list()

    def __repr__(self):
        return 'Frame(code={}, pc={}, operands={}, slots={})'.format(repr(self._code), repr(self._pc), repr(self._operands), repr(self._slots))

    def __str__(self):
        if self._pc < len(self._code):
            inst = self._code[self._pc]
            for o in dir(opcodes):
                if o.startswith('OP_') and opcodes.__dict__[o] == inst:
                    inst = o[3:]
        else:
            inst = None
        operands = '\n    '.join(str(i) + ': ' + repr(self._operands[i]) for i in range(len(self._operands)))
        slots = '\n    '.join(str(i) + ': ' + repr(self._slots[i]) for i in range(len(self._slots)))
        return 'Frame:\n  pc: {}\n  next: {}\n  operands:\n    {}\n  slots:\n    {}'.format(self._pc, inst, operands, slots)

    def get_code(self):
        return self._code

    def set_pc(self, pc):
        self._pc = pc

    def get_pc(self):
        return self._pc

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
