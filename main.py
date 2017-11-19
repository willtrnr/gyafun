#! /usr/bin/env python3

import pickle
import sys
from constant import Constant
from machine import Machine

def load_exec(path):
    with open(path, 'rb') as f:
        # TODO implement an actual binary format
        for key, value in pickle.load(f):
            key = (Constant(key[0]), key[1])
            if key[0] == Constant.SYMBOL:
                value = (Constant(value[0]), value[1])
            elif key[0] == Constant.CODE and len(value) == 2:
                value = tuple(value) + (dict(),) # Auto-upgrade
            elif key[0] == Constant.CODE:
                value = (value[0], value[1], dict(value[2]))
            yield (key, value)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} FILE'.format(sys.argv[0]))
        sys.exit(1)
    else:
        args = sys.argv[1:]
        vm = Machine(dict(load_exec(sys.argv[1])))
        ret = vm.run('main', len(args), args)
        if isinstance(ret, int):
            sys.exit(ret)
