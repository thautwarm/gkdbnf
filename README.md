# paperbnf

`pip install paperbnf`.

Maybe the most simplest way to write pretty BNF in LaTex.

Use this package with `GKD`:

```tex
\begin{GDKBNF}{lang-name}
<a> ::= a b | c
| d <a>

\end{GDKBNF}
```

```python
import paperbnf
print(paperbnf.parse("""
<nonterm> ::= term !escapeterm! | !|!
| <nonterm>

description <nonterm> ::= term !escapeterm! | !|!
| <nonterm>
"""))
```

**P.S.1**: Remember to place a new line in the end of the file, this is a must(I made this to avoid unexpected line end by force).

**P.S.2**: Paste the contents of `paperbnf.tex` to your LaTeX source:

```tex
\newcommand{\bnfdef}{ ::= }
\newcommand{\bnfistypeof}{ $\in$ }
\newcommand{\bnftype}[1]{ $ \mathtt{#1} $ }
\newcommand{\bnfalt}{ | }
\newcommand{\bnfnonterm}[1]{  $ #1 $ }
\newcommand{\bnfterm}[1]{  #1 }
\newcommand{\bnfspace}{  \quad }
\newcommand{\bnfdescr}[1]{ #1  }
\newcommand{\bnflabel}[1]{ #1 }
```

