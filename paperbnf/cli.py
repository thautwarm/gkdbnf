import argser
from paperbnf.generate import MK
from paperbnf.parser_wrap import parse
import re

comment = re.compile(r'#[^\n\r]*')


def f(filename: str):
    with open(filename) as f:
        source = f.read()

    prods = parse(comment.sub('', source), filename)
    MK().process(prods)
    return 0


def main():
    argser.call(f)
