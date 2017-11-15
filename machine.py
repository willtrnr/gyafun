import native
from constant import Constant
from frame import Frame
from handlers import ops

class Machine:

    def __init__(self, constants=None):
        self._constants = constants or dict()
        self._stack = [Frame((-1, b''))]
        self._trace = False

    def _step(self):
        frame = self.top_frame()
        op = frame.get_opcode()
        if op is None:
            return False
        if self._trace:
            print(frame.get_opcode_name())
        handler, argc = ops[op]
        args = frame.get_args(argc)
        frame.set_pc(frame.get_pc() + 1 + argc * 2)
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

    def set_trace(self, trace):
        self._trace = True if trace else False # make truthy values actually true
