import typing

from paperbnf import terms
from io import StringIO


class Backnaur:
    """
    LaTex backnaur package
    """
    def prod(self, p: terms.Prod):
        tt = (terms.Terminal, terms.Skip, terms.Eps)
        if isinstance(p.rule, terms.Alt) and not all(
                isinstance(e, tt) for e in p.rule.elts):
            io = StringIO()

            hd, *tl = p.rule.elts
            io.write(r'    \bnfprod{{{}}}{{{}}}\\'.format(
                p.name, self.rule(hd)))
            for each in tl:
                io.write('\n')
                io.write(r'    \bnfmore{{\bnfor {}}}\\'.format(
                    self.rule(each)))
            return io.getvalue()

        return r'    \bnfprod{{{}}}{{{}}}\\'.format(p.name, self.rule(p.rule))

    def nest_rule(self, *c: typing.Type[terms.Term]):
        def apply(t: terms.Term):
            base = self.rule(t)
            if isinstance(t, c):
                base = r'\bnfts{(} ' + base + r'\bnfts{)}'
            return base

        return apply

    def rule(self, t: terms.Term):
        if isinstance(t, terms.Terminal):
            n = t.name
            if not t.quoted:
                n = n[1:-1]
            n = n.replace('}', r'\}').replace('{', r'\{')
            return r"\bnftd{{{}}}".format(n)
        if isinstance(t, terms.NonTerminal):
            return r"\bnfpn{{{}}}".format(t.name)
        if isinstance(t, terms.Alt):
            return r' \bnfor '.join(map(self.nest_rule(terms.Alt), t.elts))
        if isinstance(t, terms.Seq):
            return r' \bnfsp '.join(
                map(self.nest_rule(terms.Alt, terms.Seq), t.elts))
        if isinstance(t, terms.Eps):
            return r'\bnfsp \bnfes'
        if isinstance(t, terms.Skip):
            return r'\bnksk'
        if isinstance(t, terms.Optional):
            return r'\bnfts{[} ' + self.rule(t.term) + r'\bnfts{]}'
        raise TypeError(type(t))

    @classmethod
    def process(cls, prods):
        mk = cls()
        print(r"\begin{bnf*}")
        for e in prods:
            print(mk.prod(e))
        print(r"\end{bnf*}")


class Syntax:
    """
    LaTex syntax package
    """
    def prod(self, p: terms.Prod):
        tt = (terms.Terminal, terms.Skip, terms.Eps)
        if isinstance(p.rule, terms.Alt) and not all(
                isinstance(e, tt) for e in p.rule.elts):
            io = StringIO()

            hd, *tl = p.rule.elts
            io.write(r'    <{}> : {}'.format(p.name, self.rule(hd)))
            for each in p.rule.elts:
                io.write('\n')
                io.write(r'    \alt {}'.format(self.rule(each)))
            io.write('\n')
            return io.getvalue()

        return r'    <{}> : {}'.format(p.name, self.rule(p.rule)) + '\n'

    def nest_rule(self, *c: typing.Type[terms.Term]):
        def apply(t: terms.Term):
            base = self.rule(t)
            if isinstance(t, c):
                base = '( ' + base + ' )'
            return base

        return apply

    def rule(self, t: terms.Term):
        if isinstance(t, terms.Terminal):
            n = t.name
            n = n.replace('{', '\{').replace('}', '\}')
            if t.quoted:
                n = n.replace('\\', '\\\\').replace('"', '\\' + '"')
                return r"'{}'".format(n)
            else:
                n = n[1:-1]
            return r'\textbf{{{}}}'.format(n)
        if isinstance(t, terms.NonTerminal):
            return r"<{}>".format(t.name)
        if isinstance(t, terms.Alt):
            return r' \alt '.join(map(self.nest_rule(terms.Alt), t.elts))
        if isinstance(t, terms.Seq):
            return r' '.join(map(self.nest_rule(terms.Alt, terms.Seq), t.elts))
        if isinstance(t, terms.Eps):
            return r'$\epsilon$'
        if isinstance(t, terms.Skip):
            return r'$\cdots$'
        if isinstance(t, terms.Optional):
            return r'[ ' + self.rule(t.term) + r' ]'
        raise TypeError(type(t))

    @classmethod
    def process(cls, prods):
        mk = cls()
        print(r"\begin{grammar}")
        for e in prods:
            print(mk.prod(e))
        print(r"\end{grammar}")
