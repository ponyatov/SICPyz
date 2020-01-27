## @file

## @defgroup frame extended Frame model
## @{

## Marvin Minsky's extended frame with ordered subframes
class Frame:
    def __init__(self,V):
        ## type/class tag /required for PLY parser/
        self.type = self.__class__.__name__.lower()
        ## frame name or scalar value (string,number)
        self.val  = V
        ## named slot{}s
        self.slot = {}
        ## nest[]ed ordered elements
        self.nest = []

    ## @name dump

    ## `print` callback
    def __repr__(self): return self.dump()
    ## full tree dump
    def dump(self,depth=0,prefix=''):
        tree = self._pad(depth) + self.head(prefix)
        # infty recursion
        if not depth: Frame.dumped = []
        if self in Frame.dumped: return tree + ' _/'
        else: Frame.dumped.append(self)
        # slot{}s
        for i in self.slot: tree += self.slot[i].dump(depth+1,prefix='%s = '%i)
        # nest[]ed
        idx = 0
        for j in self.nest: tree += j.dump(depth+1,prefix='%i : '%idx) ; idx += 1
        # subtree
        return tree
    ## short `<T:V>` header only dump
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix,self._type(),self._val(),id(self))
    ## pad tree dump with tabs
    def _pad(self,depth):
        return '\n' + '\t'*depth
    ## returns frame class name
    def _type(self):
        return self.type # self.__class__.__name__.lower()
    ## format `val` for dumps
    def _val(self):
        return str(self.val)

    ## @name operators

    ## `A[key]`
    def __getitem__(self,key):
        return self.slot[key]
    ## `A[key]=B`
    def __setitem__(self,key,that):
        self.slot[key] = that ; return self
    ## `A<<B --> A[B.type]=B`
    def __lshift__(self,that):
        self[that._type()] = that ; return self
    ## `A>>B --> A[B.val]=B`
    def __rshift__(self,that):
        self[that.val] = that ; return self
    ## `A//B` push
    def __floordiv__(self,that):
        self.nest.append(that) ; return self

print( Frame('Hello') // Frame('World') << Frame('left') >> Frame('right') )

## error
class Error(Frame): pass

## environment
class Env(Frame): pass
## global environment
glob = Env('global')

## primitive types
class Primitive(Frame):
    ## key property: any primitive evaluates to itself
    def eval(self,env): return self

## symbol (names of variables, methods,..)
class Symbol(Primitive): pass

## string
class String(Primitive): pass

## floating point number
class Number(Primitive): pass

## integer
class Integer(Number): pass

## hexadecimal machine number
class Hex(Integer):
    def __init__(self,V): Integer.__init__(self,int(V,0x10))
    def _val(self): return hex(self.val)

## bit stream
class Bin(Integer):
    def __init__(self,V): Integer.__init__(self,int(V,0x02))
    def _val(self): return bin(self.val)



## Data containers
class Container(Frame): pass

## List
class List(Container): pass


## EDS: executable data structures
class Active(Frame): pass

## operator
class Op(Active): pass

## function
class Fn(Active):
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def eval(self,env):
        return self.fn(env)

## input/output
class IO(Frame): pass
## disk directory
class Dir(IO): pass
## disk file
class File(IO): pass

## @}



## @defgroup web web interface
## @{

## network objects
class Net(IO): pass

## web server
class Web(Net): pass

glob << Web('flask')

print(glob)

## @}



## @defgroup ply parser
## @{

import ply.lex  as lex
import ply.yacc as yacc

## @name lexer
## @{

tokens = ['symbol','number','integer','hex','bin','lp','rp','quote']

t_ignore = '[ \t\r\n]+'
t_ignore_comment = r';.*\n'

## ( list
def t_lp(t):
    r'\('
    return t
## list )
def t_rp(t):
    r'\)'
    return t
## quote `tick
def t_quote(t):
    r'`'
    t.value = Op(t.value) ; return t

def t_exp_int(t):
    r'[+\-]?[0-9]+[eE][+\-]?[0-9]+'
    t.value = Number(t.value) ; t.type = t.value.type ; return t

def t_number(t):
    r'[+\-]?[0-9]+\.[0-9]*'
    t.value = Number(t.value) ; return t

def t_hex(t):
    r'0x[0-9a-fA-F]+'
    t.value = Hex(t.value) ; return t

def t_bin(t):
    r'0b[01]+'
    t.value = Bin(t.value) ; return t

def t_integer(t):
    r'[+\-]?[0-9]+'
    t.value = Integer(t.value) ; return t

def t_symbol(t):
    r'[^ \t\r\n\;]+'
    t.value = Symbol(t.value) ; return t

def t_ANY_error(t): raise SyntaxError(t)

lexer = lex.lex()

## @}

## @name parser
## @{

def p_REPL_none(p): ' REPL : '
def p_REPL_recur(p):
    ' REPL : REPL ex '
    print(p[2])

def p_ex_quote(p):
    ' ex : quote ex '
    p[0] = p[1] // p[2]

def p_list_empty(p):
    ' list : '
    p[0] = List('')
def p_list_item(p):
    ' list : list ex '
    p[0] = p[1] // p[2]

def p_ex_list(p):
    ' ex : lp list rp '
    p[0] = p[2]

def p_ex_sym(p):
    ' ex : symbol '
    p[0] = p[1]

def p_ex_number(p):
    ' ex : number '
    p[0] = p[1]

def p_ex_integer(p):
    ' ex : integer '
    p[0] = p[1]

def p_ex_hex(p):
    ' ex : hex '
    p[0] = p[1]

def p_ex_bin(p):
    ' ex : bin '
    p[0] = p[1]

def p_error(p): raise SyntaxError(p)

parser = yacc.yacc(debug=False, write_tables=False)

## @}

## @}



## @defgroup init system init

if __name__ == '__main__':
    import sys
    for infile in sys.argv[1:]:
        with open(infile) as src:
            parser.parse(src.read())
