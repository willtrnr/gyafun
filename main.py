import pickle
import sys
from constant import Constant
from machine import Machine

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} FILE'.format(sys.argv[0]))
        sys.exit(1)
    else:
        with open(sys.argv[1], 'rb') as f:
            pool = pickle.load(f)
            vm = Machine(dict(pool))
            ret = vm.run('main', len(sys.argv) - 1, sys.argv[1:])
            if isinstance(ret, int):
                sys.exit(ret)
