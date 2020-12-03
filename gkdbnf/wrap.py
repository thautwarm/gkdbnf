import warnings
warnings.filterwarnings('ignore', category=SyntaxWarning, message='"is" with a literal')
from gkdbnf.bnflexer import *
from gkdbnf.bnfparse import *

_parse =  mk_parser()

def parse(text: str, filename: str = "unknown", show=False, get_line_inc=lambda : 0):
    tokens = lexer(filename, text)
    status, res_or_err = _parse(None, Tokens(tokens))
    if status:
        if show:
            print(res_or_err)
        return res_or_err

    msgs = []
    lineno = None
    colno = None
    filename = None
    offset = 0
    msg = ""
    inc = get_line_inc()
    for each in res_or_err:
        i, msg = each
        token = tokens[i]
        lineno = token.lineno + inc
        colno = token.colno
        offset = token.offset
        filename = token.filename
        break
    e = SyntaxError(msg)
    e.lineno = lineno + get_line_inc()
    e.colno = colno
    e.filename = filename
    e.text = text[offset - colno:text.find('\n', offset)]
    e.offset = colno
    raise e
