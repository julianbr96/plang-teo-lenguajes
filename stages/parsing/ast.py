from rply.token import BaseBox
from llvmlite import ir

# For int variables
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
        right = self.right.eval()
        left = self.left.eval()
        internal = self.builder.add(right, left)
        return internal


class Sub(BinaryOp):
    def eval(self):
        right = self.right.eval()
        left = self.left.eval()
        internal = self.builder.sub(right, left)
        return internal


class Mul(BinaryOp):
    def eval(self):
        right = self.right.eval()
        left = self.left.eval()
        internal = self.builder.mul(right, left)
        return internal


class Div(BinaryOp):
    def eval(self):
        right = self.right.eval()
        left = self.left.eval()
        internal = self.builder.udiv(right, left)
        return internal


class Whether_not():
    def __init__(self, builder, module, predicate, then, otherwise):
        self.builder = builder
        self.module = module
        self.predicate = predicate
        self.then = then
        self.otherwise = otherwise

    def eval(self):
        with self.builder.if_else(self.predicate.eval()) as (then, otherwise):
            with then:
                self.then.eval()
            with otherwise:
                self.otherwise.eval()


class Statements():
    def __init__(self, statement=None):
        statements = [] if not statement else [statement]
        self.statements = statements

    def append(self, statement):
        # Add another statement
        self.statements.append(statement)

    def eval(self):
        # Evaluate all statements 1 by 1
        for statement in self.statements:
            statement.eval()


class Declaration():
    def __init__(self, builder, module, var_name, expression, symbol_table):
        self.builder = builder
        self.module = module
        self.value = expression
        self.var_name = var_name.value
        self.symbol_table = symbol_table

    def eval(self):
        var_ptr = self.builder.alloca(INT32)
        self.symbol_table[self.var_name] = var_ptr
        self.builder.store(self.value.eval(), var_ptr)


class Variable():
    def __init__(self, builder, module, variable, symbol_table):
        self.builder = builder
        self.module = module
        self.variable = variable
        self.symbol_table = symbol_table

    def eval(self):
        var_name = self.variable.value
        pointer = self.symbol_table.get(var_name, None)
        if not pointer:
            raise AssertionError(
                f"The var '{var_name}' in line: {self.var.source_pos} is not defined")
        value = self.builder.load(pointer)
        return value


class Predicate():
    def __init__(self, builder, module, pred_op, left, right):
        self.builder = builder
        self.module = module
        self.pred_op = pred_op
        self.left = left
        self.right = right

    def eval(self):
        pred_op = self.pred_op
        i = self.builder.icmp_unsigned(
            pred_op, self.left.eval(), self.right.eval())
        return i


class Iterator():
    def __init__(self, builder, module, predicate, block):
        self.builder = builder
        self.module = module
        self.predicate = predicate
        self.block = block

    def eval(self):
        body = self.builder.append_basic_block("iterator_expression")
        after = self.builder.append_basic_block("iterator_after")

        self.builder.cbranch(self.predicate.eval(),
                             body, after)
        self.builder.position_at_start(body)
        self.block.eval()
        self.builder.cbranch(self.predicate.eval(),
                             body, after)
        self.builder.position_at_start(after)


class Assign():
    def __init__(self, builder, module, variable, value, symbol_table):
        self.builder = builder
        self.module = module
        self.variable = variable
        self.value = value
        self.symbol_table = symbol_table

    def eval(self):
        var_name = self.variable.variable.value
        var_ptr = self.symbol_table.get(var_name, None)
        if not var_ptr:
            raise AssertionError(
                f"The var '{var_name}' in line: {self.var.source_pos} is not defined")
        self.builder.store(self.value.eval(), var_ptr)


class GiveBack():
    def __init__(self, builder, module, expression):
        self.builder = builder
        self.module = module
        self.expression = expression

    def eval(self):
        i = self.builder.ret(self.expression.eval())
        return i
