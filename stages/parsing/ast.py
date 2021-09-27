from rply.token import BaseBox
from llvmlite import ir

INT32 = ir.IntType(32)


class Number(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        internal = ir.Constant(INT32, int(self.value))
        return internal


class BinaryOp(BaseBox):
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self):
        internal = self.builder.add(self.left.eval(), self.right.eval())
        return internal


class Sub(BinaryOp):
    def eval(self):
        internal = self.builder.sub(self.left.eval(), self.right.eval())
        return internal


class Mul(BinaryOp):
    def eval(self):
        internal = self.builder.mul(self.left.eval(), self.right.eval())
        return internal


class Div(BinaryOp):
    def eval(self):
        internal = self.builder.udiv(self.left.eval(), self.right.eval())
        return internal
