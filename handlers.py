from constant import Constant
from opcodes import *

ops = [(None, 0)] * 0xFF

# General

def nop(frame, machine):
    pass
ops[OP_NOP] = (nop, 0)

# Frame control

def ret(frame, machine):
    val = frame.pop_operand()
    machine.pop_frame()
    machine.top_frame().push_operand(val)
ops[OP_RET] = (ret, 0)

# Stack management

def ld0(frame, machine):
    frame.push_operand(0)
ops[OP_LD0] = (ld0, 0)

def ld1(frame, machine):
    frame.push_operand(1)
ops[OP_LD1] = (ld1, 0)

def ldn(frame, machine):
    frame.push_operand(None)
ops[OP_LDN] = (ldn, 0)

def ldc(frame, machine, const):
    val = machine.get_constant(Constant.VALUE, const)
    frame.push_operand(val)
ops[OP_LDC] = (ldc, 1)

def ldl(frame, machine, idx):
    val = frame.get_slot(idx)
    frame.push_operand(val)
ops[OP_LDL] = (ldl, 1)

def st0(frame, machine, idx):
    frame.set_slot(idx, 0)
ops[OP_ST0] = (st0, 1)

def st1(frame, machine, idx):
    frame.set_slot(idx, 1)
ops[OP_ST1] = (st1, 1)

def stn(frame, machine, idx):
    frame.set_slot(idx, None)
ops[OP_STN] = (stn, 1)

def stc(frame, machine, idx, const):
    val = machine.get_constant(Constant.VALUE, const)
    frame.set_slot(idx, val)
ops[OP_STC] = (stc, 2)

def stl(frame, machine, idx):
    val = frame.pop_operand()
    frame.set_slot(idx, val)
ops[OP_STL] = (stl, 1)

def pop(frame, machine):
    frame.pop_operand()
ops[OP_POP] = (pop, 0)

def dup(frame, machine):
    val = frame.pop_operand()
    frame.push_operand(val)
    frame.push_operand(val)
ops[OP_DUP] = (dup, 0)

# Bitwise

def bnd(frame, machine):
    a = frame.pop_operand()
    b = frame.pop_operand()
    frame.push_operand(b & a)
ops[OP_BND] = (bnd, 0)

def bor(frame, machine):
    a = frame.pop_operand()
    b = frame.pop_operand()
    frame.push_operand(b | a)
ops[OP_BOR] = (bor, 0)

def bxr(frame, machine):
    a = frame.pop_operand()
    b = frame.pop_operand()
    frame.push_operand(b ^ a)
ops[OP_BXR] = (bxr, 0)

def bnt(frame, machine):
    val = frame.pop_operand()
    frame.push_operand(~val)
ops[OP_BNT] = (bnt, 0)

def bls(frame, machine, amount):
    val = frame.pop_operand()
    frame.push_operand(val << amount)
ops[OP_BLS] = (bls, 1)

def brs(frame, machine, amount):
    val = frame.pop_operand()
    frame.push_operand(val >> amount)
ops[OP_BRS] = (brs, 1)

# Arithmetics

def add(frame, machine):
    a = frame.pop_operand()
    b = frame.pop_operand()
    frame.push_operand(b + a)
ops[OP_ADD] = (add, 0)

def sub(frame, machine):
    a = frame.pop_operand()
    b = frame.pop_operand()
    frame.push_operand(b - a)
ops[OP_SUB] = (sub, 0)

def mul(frame, machine):
    a = frame.pop_operand()
    b = frame.pop_operand()
    frame.push_operand(b * a)
ops[OP_MUL] = (mul, 0)

def div(frame, machine):
    a = frame.pop_operand()
    b = frame.pop_operand()
    frame.push_operand(b / a)
ops[OP_DIV] = (div, 0)

def mod(frame, machine):
    a = frame.pop_operand()
    b = frame.pop_operand()
    frame.push_operand(b % a)
ops[OP_MOD] = (mod, 0)

def neg(frame, machine):
    val = frame.pop_operand()
    frame.push_operand(-val)
ops[OP_NEG] = (neg, 0)

def cmp(frame, machine):
    a = frame.pop_operand()
    b = frame.pop_operand()
    if b > a:
        frame.push_operand(1)
    elif b < a:
        frame.push_operand(-1)
    else:
        frame.push_operand(0)
ops[OP_CMP] = (cmp, 0)

# Jumps

def jmp(frame, machine, address):
    frame.set_pc(address)
ops[OP_JMP] = (jmp, 1)

def ivk(frame, machine, idx, argc):
    code = machine.get_constant(Constant.CODE, idx)
    args = [frame.pop_operand() for x in range(argc)]
    args.reverse()
    machine.invoke(code, args)
ops[OP_IVK] = (ivk, 2)

# Branching

def izr(frame, machine, address):
    val = frame.pop_operand()
    if val == 0:
        frame.set_pc(address)
ops[OP_IZR] = (izr, 1)

def inz(frame, machine, address):
    val = frame.pop_operand()
    if val != 0:
        frame.set_pc(address)
ops[OP_INZ] = (inz, 1)

def ieq(frame, machine, address):
    a = frame.pop_operand()
    b = frame.pop_operand()
    if b == a:
        frame.set_pc(address)
ops[OP_IEQ] = (ieq, 1)

def ine(frame, machine, address):
    a = frame.pop_operand()
    b = frame.pop_operand()
    if b != a:
        frame.set_pc(address)
ops[OP_INE] = (ine, 1)

def ilt(frame, machine, address):
    a = frame.pop_operand()
    b = frame.pop_operand()
    if b < a:
        frame.set_pc(address)
ops[OP_ILT] = (ilt, 1)

def igt(frame, machine, address):
    a = frame.pop_operand()
    b = frame.pop_operand()
    if b > a:
        frame.set_pc(address)
ops[OP_IGT] = (igt, 1)

def iin(frame, machine, address):
    val = frame.pop_operand()
    if val is None:
        frame.set_pc(address)
ops[OP_IIN] = (iin, 1)

def inn(frame, machine, address):
    val = frame.pop_operand()
    if val is not None:
        frame.set_pc(address)
ops[OP_INN] = (inn, 1)
