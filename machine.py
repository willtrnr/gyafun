import native
from constant import Constant
from frame import Frame
from handlers import ops

class Machine:

    def __init__(self, constants=None):
        self._constants = constants or dict()
        self._stack = [Frame((-1, b''))]
        self._interceptor = None

    def _step(self):
        frame = self.top_frame()
        op = frame.get_opcode()
        if op is None:
            return False
        handler, argc = ops[op]
        args = frame.get_args(argc)
        frame.set_next_pc(frame.get_pc() + 1 + argc * 2)
        if self._interceptor:
            self._interceptor(frame, self, handler, args)
        else:
            handler(frame, self, *args)
        frame.set_pc(frame.get_next_pc())
        return True

    def invoke(self, code_idx, args=[]):
        is_native, code, srcmap = self.get_constant(Constant.CODE, code_idx)
        if is_native:
            native.handlers[code](self.top_frame(), self, *args)
        else:
            self._stack.append(Frame((code_idx, code, srcmap), slots=[a for a in args]))

    def run(self, proc, *args):
        symbol = self.get_constant(Constant.SYMBOL, proc)
        self.invoke(symbol[1], args)
        try:
            while self._step(): pass # Main loop
            return self.top_frame().pop_operand()
        except Exception:
            for f in self._stack[1:]: print(f)
            raise

    def top_frame(self):
        return self._stack[-1]

    def pop_frame(self):
        return self._stack.pop()

    def get_constant(self, kind, idx):
        return self._constants.get((kind, idx))

    def set_interceptor(self, interceptor):
        self._interceptor = interceptor

    def set_interceptor_once(self, interceptor):
        def once(frame, machine, handler, args):
            interceptor(frame, machine, handler, args)
            machine.set_interceptor(None)
        self._interceptor = once
