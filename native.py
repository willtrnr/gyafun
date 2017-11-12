handlers = dict()

def io_print(frame, machine, value):
    print(value, end='')
    frame.push_operand(None)

handlers['io.print'] = io_print

def io_println(frame, machine, value):
    print(value)
    frame.push_operand(None)

handlers['io.println'] = io_println
