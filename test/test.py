from paperbnf.parser_wrap import parse
from paperbnf.package import Backnaur

ls = parse("""

Fun : 'function' Name FunArgs 'where' '{' Symbols '}' [Stmts] 'end';

""")

mk = Backnaur()
for e in ls:
    print(mk.prod(e))