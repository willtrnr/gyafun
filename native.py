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

# List

def list_new(frame, machine):
    frame.push_operand(list())
handlers['list.new'] = list_new

def list_push(frame, machine, lst, value):
    lst.append(value)
    frame.push_operand(None)
handlers['list.push'] = list_push

def list_at(frame, machine, lst, idx):
    frame.push_operand(lst[idx])
handlers['list.at'] = list_at

def list_size(frame, machine, lst):
    frame.push_operand(len(lst))
handlers['list.size'] = list_size

# Map

def map_new(frame, machine):
    frame.push_operand(dict())
handlers['map.new'] = map_new

def map_put(frame, machine, table, key, value):
    table[key] = value
    frame.push_operand(None)
handlers['map.put'] = map_put

def map_get(frame, machine, table, key):
    frame.push_operand(table.get(key))
handlers['map.get'] = map_get

def map_contains(frame, machine, table, key):
    frame.push_operand(1 if key in table else 0)
handlers['map.contains'] = map_contains

def map_size(frame, machine, table):
    frame.push_operand(len(table))
handlers['map.size'] = map_size

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
