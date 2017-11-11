handlers = dict()

def native_print(frame, machine, value):
    print(value)
    frame.push_operand(None)

handlers['print'] = native_print
