import sys
import regex
import opcodes

OPS = {o[3:]: opcodes.__dict__[o] for o in dir(opcodes) if o.startswith('OP_')}

COMMENTS_RE = regex.compile(r';.*')
INSTRUCTION_RE = regex.compile(r'^([A-Z]{3})(?:\s+((?:0x)?[0-9]+))*$', re.I)

def read_lines(*paths):
    for p in paths:
        with open(p, 'r') as f:
            for line in f:
                line = COMMENTS_RE.sub('', line).strip()
                if line:
                    yield line

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} FILE [FILE [FILE [...]]]'.format(sys.argv[0]))
        sys.exit(1)
    else:
        with open('a.out', 'wb') as f:
            for line in read_lines(*sys.argv[1:]):
                match = INSTRUCTION_RE.match(line)
                if match:
                    f.write(OPS[match.group(1)].to_bytes(1, byteorder='little'))
                    for a in match.captures(2):
                        f.write(int(a).to_bytes(2, byteorder='little'))
