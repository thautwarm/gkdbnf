# paperbnf

`pip install paperbnf`.

Maybe the most simpest way to write pretty BNF in LaTex.

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

**P.S**: Remember to place a new line in the end of the file, this is a must(I made this to avoid unexpected line end by force).

