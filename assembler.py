#! /usr/bin/env python3

import opcodes
import pickle
import regex
import sys
from enum import Enum
from machine import Constant

class Statement(Enum):
    CONST = 0x01
    LABEL = 0x02
    INST = 0x03

class Argument(Enum):
    LITERAL = 0x01
    IDENT = 0x02

OPS = {o[3:]: opcodes.__dict__[o] for o in dir(opcodes) if o.startswith('OP_')}

IDENT = r'\.?[A-Za-z_][A-Za-z0-9_\.\$\-]*'
NUM_LIT = r'0x[0-9A-Fa-f]+|[0-9A-Fa-f]+h|-?[0-9]+d?'
FLT_LIT = r'-?[0-9]+\.[0-9]*|-?\.[0-9]+'
STR_LIT = r'"((?:\\"|.)*?)"'
CHR_LIT = r"'(\\?.)'"
COMMENTS = r'\s*(?:;.*)?$'

CONST_RE = regex.compile(r'^(' + IDENT + r'):\s+(?:(native(?:\s+(' + IDENT + r'))?)|(' + FLT_LIT + r')|(' + NUM_LIT + r')|' + CHR_LIT + r'|' + STR_LIT + r')' + COMMENTS)
LABEL_RE = regex.compile(r'^(' + IDENT + r'):' + COMMENTS)
ALIAS_RE = regex.compile(r'^\$(' + IDENT + r')\s+(' + NUM_LIT + r'|' + IDENT + r')' + COMMENTS)
INSTRUCTION_RE = regex.compile(r'^(' + IDENT + r')(?:\s+(' + NUM_LIT + r'|\$?' + IDENT + r'))*' + COMMENTS)

def read_lines(paths, mode='r'):
    for p in paths:
        with open(p, mode) as f:
            for line in f:
                yield line

def parse_literal(value):
    if value.startswith('0x'):
        return int(value[2:], 16)
    elif value.endswith('h'):
        return int(value[:-1], 16)
    elif value.endswith('d'):
        return int(value[:-1])
    else:
        return int(value)

def parse_arg(arg, aliases=dict()):
    if arg.startswith('$'):
        return aliases[arg[1:]]
    else:
        try:
            return (Argument.LITERAL, parse_literal(arg))
        except:
            return (Argument.IDENT, arg)

def read_stmts(lines):
    aliases = dict()
    for src_line in lines:
        line = src_line.strip()
        const = CONST_RE.match(line)
        if const:
            if const.group(2):
                yield (Statement.CONST, const.group(1), Constant.CODE, (True, const.group(3) or const.group(1)))
            elif const.group(4) is not None:
                yield (Statement.CONST, const.group(1), Constant.VALUE, float(const.group(4)))
            elif const.group(5) is not None:
                yield (Statement.CONST, const.group(1), Constant.VALUE, parse_literal(const.group(5)))
            elif const.group(6) is not None:
                yield (Statement.CONST, const.group(1), Constant.VALUE, ord(bytes(const.group(6), 'utf-8').decode('unicode_escape')[0]))
            elif const.group(7) is not None:
                yield (Statement.CONST, const.group(1), Constant.VALUE, bytes(const.group(7), 'utf-8').decode('unicode_escape'))
        else:
            label = LABEL_RE.match(line)
            if label:
                yield (Statement.LABEL, label.group(1))
            else:
                alias = ALIAS_RE.match(line)
                if alias:
                    aliases[alias.group(1)] = parse_arg(alias.group(2), aliases)
                else:
                    inst = INSTRUCTION_RE.match(line)
                    if inst:
                        args = [parse_arg(a, aliases) for a in inst.captures(2)] if inst.captures(2) else list()
                        yield (Statement.INST, inst.group(1).upper(), args)

def assemble(stmts, pool=None, reverse_pool=None):
    pool = pool or dict()
    reverse_pool = reverse_pool or dict()

    labels = dict()
    symbols = dict()

    try:
        code_idx = max(pool.keys(), key=lambda c: c[1] if c[0] == Constant.CODE else -1) + 1
    except:
        code_idx = 0
    try:
        value_idx = max(pool.keys(), key=lambda c: c[1] if c[0] == Constant.VALUE else -1) + 1
    except:
        value_idx = 0

    # First pass: mostly compute label positions and identifier values
    pos = 0
    current = None
    for stmt in stmts:
        if stmt[0] == Statement.CONST:
            if stmt[2] == Constant.CODE:
                if (stmt[2], stmt[1]) not in pool:
                    if (stmt[2], stmt[3]) in reverse_pool:
                        pool[stmt[2], stmt[1]] = reverse_pool[stmt[2], stmt[3]]
                    else:
                        pool[stmt[2], stmt[1]] = code_idx
                        reverse_pool[stmt[2], stmt[3]] = code_idx
                        yield ((Constant.CODE, code_idx), stmt[3])
                        code_idx += 1
            elif stmt[2] == Constant.VALUE:
                name = (current, stmt[1]) if stmt[1].startswith('.') else stmt[1]
                if (stmt[2], name) not in pool:
                    if (stmt[2], stmt[3]) in reverse_pool:
                        pool[stmt[2], name] = reverse_pool[stmt[2], stmt[3]]
                    else:
                        pool[stmt[2], name] = value_idx
                        reverse_pool[stmt[2], stmt[3]] = value_idx
                        yield ((Constant.VALUE, value_idx), stmt[3])
                        value_idx += 1
        elif stmt[0] == Statement.LABEL:
            if stmt[1].startswith('.'):
                labels[current, stmt[1]] = pos
            else:
                pos = 0
                current = stmt[1]
                symbols[current] = list()
                pool[Constant.CODE, current] = code_idx
                code_idx += 1
        elif stmt[0] == Statement.INST:
            symbols[current].append((OPS[stmt[1]], stmt[2]))
            pos += 1 + len(stmt[2]) * 2

    # Second pass: output code
    for symbol, code in symbols.items():
        buf = b''
        for op, args in code:
            buf += op.to_bytes(1, byteorder='little')
            for arg in args:
                if arg[0] == Argument.LITERAL:
                    buf += arg[1].to_bytes(2, byteorder='little')
                elif arg[0] == Argument.IDENT:
                    if (symbol, arg[1]) in labels:
                        buf += labels[symbol, arg[1]].to_bytes(2, byteorder='little')
                    else:
                        name = (symbol, arg[1]) if arg[1].startswith('.') else arg[1]
                        if (Constant.VALUE, name) in pool:
                            buf += pool[Constant.VALUE, name].to_bytes(2, byteorder='little')
                        elif (Constant.CODE, name) in pool:
                            buf += pool[Constant.CODE, name].to_bytes(2, byteorder='little')
                        else:
                            pool[Constant.CODE, arg[1]] = code_idx
                            buf += code_idx.to_bytes(2, byteorder='little')
                            code_idx += 1
        idx = pool[Constant.CODE, symbol]
        yield ((Constant.CODE, idx), (False, buf))
        yield ((Constant.SYMBOL, symbol), (Constant.CODE, idx))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} FILE [FILE [FILE [...]]]'.format(sys.argv[0]))
        sys.exit(1)
    else:
        with open('a.out', 'wb') as f:
            global_pool = dict()
            global_reverse_pool = dict()
            parts = list()
            for part in assemble(read_stmts(read_lines(sys.argv[1:])), global_pool, global_reverse_pool):
                print(part)
                parts.append(part)
            # TODO make an actual binary file format
            pickle.dump(parts, f)
