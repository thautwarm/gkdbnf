from gkdbnf.wrap import parse
from wisepy2 import wise
from pathlib import Path

def tobnf(filename: str, mkdir: bool = False):
    if mkdir:
        Path(filename).parent.mkdir(mode=0o777, parents=True, exist_ok=True)
        return
    with open(filename, 'r') as f:
        print(parse(f.read(), filename))

def main():
    wise(tobnf)()
