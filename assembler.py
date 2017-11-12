import sys
import regex
import opcodes
from enum import Enum

class Statement(Enum):
    CONST = 0x01
    LABEL = 0x02
    INST = 0x03

class Argument(Enum):
    LITERAL = 0x01
    IDENT = 0x02

OPS = {o[3:]: opcodes.__dict__[o] for o in dir(opcodes) if o.startswith('OP_')}

NUM_LIT = r'0x[0-9A-F]+|[0-9A-F]h|[0-9]d?'
STR_LIT = r'"(?:\\"|.)*?"'
IDENT = r'\.?[A-Za-z][A-Za-z0-9_\.]*'

COMMENTS_RE = regex.compile(r';.*')
INSTRUCTION_RE = regex.compile(r'^(' + IDENT + r')(?:\s+(' + NUM_LIT + r'|\$?' + IDENT + r'))*$')
LABEL_RE = regex.compile(r'^(' + IDENT + r'):$')
CONST_RE = regex.compile(r'^(' + IDENT + r'):\s+(?:(?:(native(?: ' + IDENT + r')?))|(' + NUM_LIT + r')|(' + STR_LIT + r'))$')
ALIAS_RE = regex.compile(r'^\$(' + IDENT + r')\s+(' + NUM_LIT + r'|' + IDENT + r')$')

def read_lines(paths, mode='r'):
    for p in paths:
        with open(p, mode) as f:
            for line in f:
                yield line

def parse_arg(arg, aliases=dict()):
    if arg.startswith('$'):
        return aliases[arg[1:]]
    if arg.startswith('0x'):
        return (Argument.LITERAL, int(arg[2:], 16))
    elif arg.endswith('h'):
        return (Argument.LITERAL, int(arg[:-1], 16))
    elif arg.endswith('d'):
        return (Argument.LITERAL, int(arg[:-1]))
    else:
        try:
            return (Argument.LITERAL, int(arg))
        except:
            return (Argument.IDENT, arg)

def read_stmts(lines):
    aliases = dict()
    for src_line in lines:
        line = COMMENTS_RE.sub('', src_line).strip()
        const = CONST_RE.match(line)
        if const:
            yield (Statement.CONST, const.group(1), const.group(2) or const.group(3) or const.group(4))
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

def assemble(stmts, pool=dict()):
    labels = dict()
    symbols = dict()
    current = None
    pos = 0
    for stmt in stmts:
        if stmt[0] == Statement.CONST:
            pool[stmt[1]] = len(pool) + 1 # TODO
        elif stmt[0] == Statement.LABEL:
            if stmt[1].startswith('.'):
                labels[current, stmt[1]] = pos
            else:
                pos = 0
                current = stmt[1]
                symbols[current] = list()
        elif stmt[0] == Statement.INST:
            symbols[current].append((OPS[stmt[1]], stmt[2]))
            pos += 1 + len(stmt[2]) * 2
    for symbol, code in symbols.items():
        for op, args in code:
            buf = op.to_bytes(1, byteorder='little')
            for arg in args:
                if arg[0] == Argument.LITERAL:
                    buf += arg[1].to_bytes(2, byteorder='little')
                elif arg[0] == Argument.IDENT:
                    if (symbol, arg[1]) in labels:
                        buf += labels[symbol, arg[1]].to_bytes(2, byteorder='little')
                    else:
                        if arg[1] not in pool:
                            pool[arg[1]] = len(pool) + 1
                        buf += pool[arg[1]].to_bytes(2, byteorder='little')
            yield buf

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} FILE [FILE [FILE [...]]]'.format(sys.argv[0]))
        sys.exit(1)
    else:
        with open('a.out', 'wb') as f:
            for inst in assemble(read_stmts(read_lines(sys.argv[1:]))):
                f.write(inst)
