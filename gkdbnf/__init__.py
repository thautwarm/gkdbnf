def bnf(src, *, self, tex_print, opts = "lllllll"):
    import gkdtex.developer_utilities as dev
    from gkdbnf.wrap import parse
    if not isinstance(opts, str):
        opts = dev.eval_to_string(self, opts.obj)
    l = src.offs[0]
    def get_line_inc():
        return self.src[:l].count('\n')
    tex_print("\\begin{tabular}{%s}\n" % opts)
    tex_print(parse(dev.get_raw_from_span_params(self.src, src.offs), self.filename,  get_line_inc=get_line_inc))
    tex_print('\n')
    tex_print("\\end{tabular}\n")

class GkdInterface:
    @staticmethod
    def load(self, tex_print):
        tex_print(
        r"""
\newcommand{\bnfdef}{ ::= }
\newcommand{\bnfistypeof}{ $\in$ }
\newcommand{\bnftype}[1]{ $\mathtt{#1}$ }
\newcommand{\bnfalt}{ $\mathrm{|}$ }
\newcommand{\bnfnonterm}[1]{  $\mathit{#1}$ }
\newcommand{\bnfterm}[1]{  $\mathrm{#1}$ }
\newcommand{\bnfspace}{ $\!\!\!\!$  }
\newcommand{\bnfdescr}[1]{ #1  }
\newcommand{\bnflabel}[1]{ #1 }
        """)
        self.globals['gkd@bnf'] = bnf
