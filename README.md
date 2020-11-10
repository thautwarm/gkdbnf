# paperbnf

`pip install paperbnf`.

```python
import paperbnf
paperbnf.parse("""
<nonterm> ::= term !escapeterm! | !|!
| <nonterm>

description <nonterm> ::= term !escapeterm! | !|!
| <nonterm>
""")

```
