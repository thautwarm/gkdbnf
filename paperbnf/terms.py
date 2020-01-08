from dataclasses import dataclass
import typing


@dataclass
class Terminal:
    name: str


@dataclass
class NonTerminal:
    name: str


@dataclass
class Optional:
    term: 'Term'


@dataclass
class Eps:
    pass

@dataclass
class Skip:
    pass

@dataclass
class Seq:
    elts: typing.List['Term']


@dataclass
class Alt:
    elts: typing.List['Term']

@dataclass
class Prod:
    name: str
    rule: 'Term'


Term = typing.Union[Optional, Terminal, NonTerminal, Eps, Seq, Alt, Skip]


def seq(xs):
    assert xs
    if len(xs) is 1:
        return xs[0]
    return Seq(xs)


def alt(xs):
    assert xs
    if len(xs) is 1:
        return xs[0]
    return Alt(xs)
