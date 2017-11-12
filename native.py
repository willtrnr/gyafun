handlers = dict()

def io_print(frame, machine, value):
    if isinstance(value, (bytes, bytearray)):
        value = value.decode('utf-8')
    print(value, end='')
    frame.push_operand(None)
handlers['io.print'] = io_print

def io_println(frame, machine, value):
    if isinstance(value, (bytes, bytearray)):
        value = value.decode('utf-8')
    print(value)
    frame.push_operand(None)
handlers['io.println'] = io_println

def io_fopen(frame, machine, path, mode='r'):
    try:
        frame.push_operand(open(path, mode + 'b'))
    except:
        frame.push_operand(None)
handlers['io.fopen'] = io_fopen

def io_fread(frame, machine, f, size):
    try:
        data = f.read(size)
        if data:
            frame.push_operand(data)
        else:
            frame.push_operand(None)
    except:
        frame.push_operand(None)
handlers['io.fread'] = io_fread

def io_fclose(frame, machine, f):
    f.close()
    frame.push_operand(None)
handlers['io.fclose'] = io_fclose

def arr_at(frame, machine, arr, idx):
    frame.push_operand(arr[idx])
handlers['arr.at'] = arr_at
