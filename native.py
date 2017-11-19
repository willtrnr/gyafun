import os
import sys
import regex
import pickle

def strlike(value):
    try:
        return value.decode('utf-8')
    except:
        return value

# C-like functions stuff mostly

handlers = dict()
def register(name):
    def wrap(handler):
        handlers[name] = handler
        return handler
    return wrap

# String

@register('str.substr')
def str_substr(frame, machine, s, start, stop):
    frame.push_operand(s[start:stop])

@register('str.unescape')
def str_unescape(frame, machine, s):
    frame.push_operand(bytes(s, 'utf-8').decode('unicode_escape'))

# Int

@register('int.to_bytes')
def int_to_bytes(frame, machine, i, size):
    frame.push_operand(i.to_bytes(size, byteorder='little'))

# Regex

@register('regex.compile')
def regex_compile(frame, machine, pattern):
    frame.push_operand(regex.compile(strlike(pattern)))

@register('regex.match')
def regex_match(frame, machine, pattern, value):
    match = pattern.match(strlike(value))
    if match:
        frame.push_operand([match.group()] + list(match.groups()))
    else:
        frame.push_operand(None)

@register('regex.replace')
def regex_replace(frame, machine, pattern, value, replace):
    frame.push_operand(pattern.sub(strlike(replace), strlike(value)))

@register('regex.split')
def regex_split(frame, machine, pattern, value):
    frame.push_operand(pattern.split(strlike(value)))

# I/O related stuff

@register('io.print')
def io_print(frame, machine, value):
    sys.stdout.write(strlike(value))
    frame.push_operand(None)

@register('io.println')
def io_println(frame, machine, value):
    sys.stdout.write(strlike(value) + os.linesep)
    frame.push_operand(None)

@register('io.printf')
def io_printf(frame, machine, pattern, *args):
    sys.stdout.write(strlike(pattern) % args)
    frame.push_operand(None)

@register('io.fopen')
def io_fopen(frame, machine, path, mode):
    try:
        frame.push_operand(open(strlike(path), strlike(mode) + 'b'))
    except:
        frame.push_operand(None)

@register('io.fread')
def io_fread(frame, machine, f, size):
    data = f.read(size)
    if data:
        frame.push_operand(data)
    else:
        frame.push_operand(None)

@register('io.freadline')
def io_freadline(frame, machine, f):
    data = f.readline()
    if data:
        frame.push_operand(data)
    else:
        frame.push_operand(None)

@register('io.fclose')
def io_fclose(frame, machine, f):
    f.close()
    frame.push_operand(None)

# Pickle, until I make a real file format

@register('pickle.dump')
def pickle_dump(frame, machine, obj, f):
    pickle.dump(obj, f)
    frame.push_operand(None)

@register('pickle.dumps')
def pickle_dumps(frame, machine, obj):
    frame.push_operand(pickle.dumps(obj))

@register('pickle.load')
def pickle_load(frame, machine, f):
    frame.push_operand(pickle.load(f))

@register('pickle.loads')
def pickle_loads(frame, machine, s):
    frame.push_operand(pickle.load(s))
