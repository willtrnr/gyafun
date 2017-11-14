import native
from constant import Constant
from frame import Frame
from handlers import ops

class Machine:

    def __init__(self, constants=None):
        self._constants = constants or dict()
        self._stack = [Frame((-1, b''))]

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

    def invoke(self, code_idx, args=[]):
        is_native, code = self.get_constant(Constant.CODE, code_idx)
        if is_native:
            native.handlers[code](self.top_frame(), self, *args)
        else:
            self._stack.append(Frame((code_idx, code), slots=[a for a in args]))

    def run(self, proc, *args):
        symbol = self.get_constant(Constant.SYMBOL, proc)
        self.invoke(symbol[1], args)
        try:
            while self._step(): pass # Main loop
            return self.top_frame().pop_operand()
        except Exception as e:
            for f in self._stack:
                print(f)
            raise e

    def top_frame(self):
        return self._stack[-1]

    def pop_frame(self):
        return self._stack.pop()

    def get_constant(self, kind, idx):
        return self._constants.get((kind, idx))
