from paperbnf.parser_wrap import parse
from paperbnf.generate import MK

ls = parse("""
A : b c d
  | e f g
  ;
C : 'a' | 'd' | 'g'
""")

mk = MK()
for e in ls:
    print(mk.prod(e))