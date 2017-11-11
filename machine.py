import native
from constant import Constant
from frame import Frame
from handlers import ops

class Machine:

    def __init__(self, constants=dict()):
        self._constants = constants
        self._stack = []

    def _step(self):
        frame = self.top_frame()
        pc = frame.get_pc()
        code = frame.get_code()
        if pc >= len(code):
            return False
        op = code[pc]
        (handler, argc) = ops[op]
        frame.set_pc(pc + 1 + argc * 2)
        args = [int.from_bytes(code[pc + 1 + x * 2:pc + 1 + (x + 1) * 2], byteorder='little', signed=False) for x in range(argc)]
        handler(frame, self, *args)
        return True

    def invoke(self, code, args=[]):
        is_native, code = code
        if is_native:
            native.handlers[code](self.top_frame(), self, *args)
        else:
            self._stack.append(Frame(code, slots={i: args[i] for i in range(len(args))}))

    def run(self, proc, *args):
        code = self.get_constant(*self.get_constant(Constant.SYMBOL, proc))
        self.invoke(code, args)
        while self._step(): pass

    def top_frame(self):
        return self._stack[-1]

    def pop_frame(self):
        return self._stack.pop()

    def get_constant(self, kind, idx):
        return self._constants.get((kind, idx))
