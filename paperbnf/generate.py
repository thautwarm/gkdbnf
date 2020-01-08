import typing

from paperbnf import terms
from io import StringIO


class MK:
    def prod(self, p: terms.Prod):
        tt = (terms.Terminal, terms.Skip, terms.Eps)
        if isinstance(p.rule, terms.Alt) and not all(
                isinstance(e, tt) for e in p.rule.elts):
            io = StringIO()

            hd, *tl = p.rule.elts
            io.write(r'    \bnfprod{{{}}}{{{}}}\\'.format(p.name, self.rule(hd)))
            for each in p.rule.elts:
                io.write('\n')
                io.write(r'    \bnfmore{{\bnfor {}}}\\'.format(self.rule(each)))
            return io.getvalue()

        return r'    \bnfprod{{{}}}{{{}}}'.format(p.name, self.rule(p.rule))

    def nest_rule(self, *c: typing.Type[terms.Term]):
        def apply(t: terms.Term):
            base = self.rule(t)
            if isinstance(t, c):
                base = r'\bnftd{(} ' + base + r'\bnftd{)}'
            return base

        return apply

    def rule(self, t: terms.Term):
        if isinstance(t, terms.Terminal):
            return r"\bnfts{{{}}}".format(t.name)
        if isinstance(t, terms.NonTerminal):
            return r"\bnfpn{{{}}}".format(t.name)
        if isinstance(t, terms.Alt):
            return r' \bnfor '.join(map(self.nest_rule(terms.Alt), t.elts))
        if isinstance(t, terms.Seq):
            return r' \bnfsp '.join(map(self.nest_rule(terms.Alt, terms.Seq), t.elts))
        if isinstance(t, terms.Eps):
            return r'\bnfes'
        if isinstance(t, terms.Skip):
            return r'\bnksk'
        if isinstance(t, terms.Optional):
            return r'\bnftd{[} ' + self.rule(t.term) + r'\bnftd{]}'
        raise TypeError(type(t))

    @classmethod
    def process(cls, prods):
        mk = MK()
        print(r"\begin{bnf*}")
        for e in prods:
            print(mk.prod(e))
        print(r"\end{bnf*}")
