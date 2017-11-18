#! /usr/bin/env python3

import pickle
import sys
from constant import Constant
from machine import Machine

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} FILE'.format(sys.argv[0]))
        sys.exit(1)
    else:
        args = sys.argv[1:]
        with open(sys.argv[1], 'rb') as f:
            # TODO implement an actual binary format
            pool = pickle.load(f)
            vm = Machine(dict(pool))
            ret = vm.run('main', len(args), args)
            if isinstance(ret, int):
                sys.exit(ret)
