from paperbnf.parser_generated import *
from paperbnf import terms
from rbnf_rts.rts import Tokens, State
import typing

__all__ = ['parse']
_parse = mk_parser(Eps=terms.Eps,
                   Terminal=terms.Terminal,
                   NonTerminal=terms.NonTerminal,
                   Optional=terms.Optional,
                   Skip=terms.Skip,
                   Prod=terms.Prod,
                   seq=terms.seq,
                   alt=terms.alt)


def parse(text: str, filename: str = "unknown") -> typing.List[terms.Prod]:
    tokens = list(run_lexer(filename, text))
    res = _parse(State(), Tokens(tokens))
    if res[0]:
        return res[1]
    msgs = []
    assert res[1]
    maxline = 0
    for each in res[1]:
        i, msg = each
        token = tokens[i]
        lineno = token.lineno
        maxline = max(lineno, maxline)
        colno = token.colno
        msgs.append(f"Line {lineno}, column {colno}, {msg}")

    e = SyntaxError()
    e.lineno = maxline + 1
    e.msg = '\n'.join(msgs)
    e.filename = filename
    e.offset = token.offset
    e.text = text
    raise e
