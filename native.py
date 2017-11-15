import os
import sys
import regex

def strlike(value):
    try:
        return value.decode('utf-8')
    except:
        return value

# C-like functions stuff mostly

handlers = dict()

# String

def str_substr(frame, machine, s, start, stop):
    frame.push_operand(s[start:stop])
handlers['str.substr'] = str_substr

def str_unescape(frame, machine, s):
    frame.push_operand(bytes(s, 'utf-8').decode('unicode_escape'))
handlers['str.unescape'] = str_unescape

# Regex

def regex_compile(frame, machine, pattern):
    frame.push_operand(regex.compile(strlike(pattern)))
handlers['regex.compile'] = regex_compile

def regex_match(frame, machine, pattern, value):
    match = pattern.match(strlike(value))
    if match:
        frame.push_operand([match.group()] + list(match.groups()))
    else:
        frame.push_operand(None)
handlers['regex.match'] = regex_match

def regex_replace(frame, machine, pattern, value, replace):
    frame.push_operand(pattern.sub(strlike(replace), strlike(value)))
handlers['regex.replace'] = regex_replace

def regex_split(frame, machine, pattern, value):
    frame.push_operand(pattern.split(strlike(value)))
handlers['regex.split'] = regex_split

# I/O related stuff

def io_print(frame, machine, value):
    sys.stdout.write(strlike(value))
    frame.push_operand(None)
handlers['io.print'] = io_print

def io_println(frame, machine, value):
    sys.stdout.write(strlike(value) + os.linesep)
    frame.push_operand(None)
handlers['io.println'] = io_println

def io_printf(frame, machine, pattern, *args):
    sys.stdout.write(strlike(pattern) % args)
    frame.push_operand(None)
handlers['io.printf'] = io_printf

def io_fopen(frame, machine, path, mode='r'):
    try:
        frame.push_operand(open(strlike(path), strlike(mode) + 'b'))
    except:
        frame.push_operand(None)
handlers['io.fopen'] = io_fopen

def io_fread(frame, machine, f, size):
    data = f.read(size)
    if data:
        frame.push_operand(data)
    else:
        frame.push_operand(None)
handlers['io.fread'] = io_fread

def io_freadline(frame, machine, f):
    data = f.readline()
    if data:
        frame.push_operand(data)
    else:
        frame.push_operand(None)
handlers['io.freadline'] = io_freadline

def io_fclose(frame, machine, f):
    f.close()
    frame.push_operand(None)
handlers['io.fclose'] = io_fclose
