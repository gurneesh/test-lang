#Abstract syntax tree
"""
In computer science, an abstract syntax tree (AST), or just syntax tree, is a tree representation of the abstract syntactic structure of source code written in a programming language. 
"""
from llvmlite import ir
from ctypes import CFUNCTYPE, c_double

class IntegerLiteral:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return __class__.__name__ + '(value=' + str(self.value) + ')'

    def to_dict(self):
        return { 'type': __class__.__name__, 'value': self.value }

    def eval(self):
        i = ir.Constant(ir.IntType(8), int(self.value))
        return i

class UnaryOpExpression:
    def __init__(self, op, rhs, module, builder, printf):
        self.op = op
        self.rhs = rhs
        self.module = module
        self.builder = builder
        self.printf = printf

    def __repr__(self):
        return __class__.__name__ + '(op=' + '\'' + self.op + '\'' + ', ' +  ' rhs=' + str(self.rhs) + ')'

    def to_dict(self):
        return { 'type': __class__.__name__, 'op': self.op, 'rhs': self.rhs.to_dict() }

    def eval(self):
        if self.op == '+':
            return self.rhs
        elif self.op == '-':
            i = ir.Constant(ir.IntType(8), int((-1)*self.value))
            return i
"""
class BinaryOp():
    def _init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left
        self.right
"""

class BinaryOpExpression:
    def __init__(self, lhs, op, rhs, module, builder, printf):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
        self.module = module
        self.builder = builder
        self.printf = printf

    def __repr__(self):
        return __class__.__name__ + '(lhs=' + str(self.lhs) + ',' + ' op=' + '\'' + self.op + '\'' + ', ' +  ' rhs=' + str(self.rhs) + ')'

    def to_dict(self):
        return { 'type': __class__.__name__, 'lhs': self.lhs.to_dict(), 'op': self.op, 'rhs': self.rhs.to_dict() }

    
    def eval(self):
        if self.op == '+':
            i = self.builder.add(self.lhs.eval(), self.rhs.eval())
            return i
        elif self.op == '-':
            i = self.builder.sub(self.lhs.eval(), self.rhs.eval())
            return i
        elif self.op == '*':
            i = self.builder.mul(self.lhs.eval(), self.rhs.eval())
            return i 
        elif self.op == '/':
            i = self.builder.sdiv(self.lhs.eval(), self.rhs.eval())
            return i
        else:
            raise NotImplementedError()

class Print():
    def __init__(self, module, builder, printf, value):
        self.module = module
        self.builder = builder
        self.printf = printf
        self.value = value
        #print('g')

    def eval(self):
        value = self.value.eval()
        print(value)
        # Declare argument list
        voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

        # Call Print Function
        self.builder.call(self.printf, [fmt_arg, value])

if __name__=='__main__':
    from llvmlite import ir, binding
    block = base_func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)
    i = BinaryOpExpression(4+5)
    print(i.eval())
