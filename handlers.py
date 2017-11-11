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

# Memory management

def ldc(frame, machine, idx):
    val = machine.get_constant(Constant.VALUE, idx)
    frame.push_operand(val)

ops[OP_LDC] = (ldc, 1)

def ldl(frame, machine, idx):
    val = frame.get_slot(idx)
    frame.push_operand(val)

ops[OP_LDL] = (ldl, 1)

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

# Jumps

def jmp(frame, machine, address):
    frame.set_pc(address)

ops[OP_JMP] = (jmp, 1)

def ivk(frame, machine, idx, argc):
    code = machine.get_constant(Constant.CODE, idx)
    machine.invoke(code, reversed([frame.pop_operand() for x in range(argc)]))

ops[OP_IVK] = (ivk, 2)

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
