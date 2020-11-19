# paperbnf

`pip install paperbnf2`.

Maybe the most simpest way to write pretty BNF in LaTex.

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

