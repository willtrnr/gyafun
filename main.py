import sys
from constant import Constant
from machine import Machine

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} FILE'.format(sys.argv[0]))
        sys.exit(1)
    else:
        with open(sys.argv[1], 'rb') as f:
            code = f.read()
            vm = Machine({(Constant.CODE, 0): (False, code),
                          (Constant.CODE, 1): (True, 'print'),
                          (Constant.VALUE, 0): 0,
                          (Constant.VALUE, 1): 1,
                          (Constant.SYMBOL, 'main'): (Constant.CODE, 0)})
            vm.run('main', len(sys.argv) - 1, sys.argv[1:])
