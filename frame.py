class Frame:
    def __init__(self, code, pc=0, operands=[], slots=dict()):
        self._code = code
        self._pc = pc
        self._operands = operands
        self._slots = slots

    def __repr__(self):
        return 'Frame(code={}, pc={}, operands={}, slots={})'.format(repr(self._code), repr(self._pc), repr(self._operands), repr(self._slots))

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
        self._slots[idx] = value

    def get_slot(self, idx):
        return self._slots.get(idx)
