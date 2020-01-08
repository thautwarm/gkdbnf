# paperbnf

Generating beautiful BNF(supporting optional `[ ... ]`) from RBNF syntax, thus the BNF file can generate parsers as well.  

## Installation

`pip install paperbnf`

## Usage

```
paperbnf <filename>
```

## Example
```shell script
sh> cat a.rbnf
a ::= a b;
b ::=  [b] c
      | a 'd' <e>
      | '$\\alpha$'
      ;

# `:` is okay
op : '+'
   | '-' 
   | '*'
   ;

# sh> paperbnf a.rbnf > <output file>
```
produces

```latex
\begin{bnf*}
    \bnfprod{a}{\bnfpn{a} \bnfsp \bnfpn{b}}
    \bnfprod{b}{\bnftd{[} \bnfpn{b}\bnftd{]} \bnfsp \bnfpn{c}}\\
    \bnfmore{\bnfor \bnftd{[} \bnfpn{b}\bnftd{]} \bnfsp \bnfpn{c}}\\
    \bnfmore{\bnfor \bnfpn{a} \bnfsp \bnfts{d} \bnfsp \bnfts{<e>}}\\
    \bnfmore{\bnfor \bnfts{$\alpha$}}\\
    \bnfprod{op}{\bnfts{+} \bnfor \bnfts{-} \bnfor \bnfts{*}}
\end{bnf*}
``` 
 

