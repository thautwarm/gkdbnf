from paperbnf_lex import *
from paperbnf_parser import *

_parse =  mk_parser()
def parse(text: str, filename: str = "unknown", show=False):
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
        lineno = token.lineno
        colno = token.colno
        msgs.append(f"line {lineno}, column {colno}, {msg}")
    raise SyntaxError(f"filename {filename}:\n" + "\n".join(msgs))
    