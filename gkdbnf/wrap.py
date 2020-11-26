import warnings
warnings.filterwarnings('ignore', category=SyntaxWarning, message='"is" with a literal')
from gkdbnf.bnflexer import *
from gkdbnf.bnfparse import *

_parse =  mk_parser()
def parse(text: str, filename: str = "unknown", show=False, get_line_inc=lambda : 0):
    tokens = lexer(filename, text)
    res = _parse(None, Tokens(tokens))
    if res[0]:
        res = res[1]
        if show: print(res)
        return res

    msgs = []
    for each in res[1]:
        i, msg = each
        token = tokens[i]
        lineno = token.lineno + get_line_inc() + 1
        colno = token.colno
        msgs.append(f"line {lineno}, column {colno}, {msg}")
    raise SyntaxError(f"filename {filename}:\n" + "\n".join(msgs))
