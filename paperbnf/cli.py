import argser
from paperbnf import package
from paperbnf.parser_wrap import parse
import re

comment = re.compile(r'#[^\n\r]*')


def f(filename: str, backend='Backnaur'):
    """
    backend: Backnaur | Syntax
    """
    be = {
        'backnaur': package.Backnaur, 'syntax': package.Syntax
    }[backend.lower()]
    with open(filename) as f:
        source = f.read()

    prods = parse(comment.sub('', source), filename)
    be().process(prods)
    return 0


def main():
    argser.call(f)
