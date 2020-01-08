# paperbnf

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
      | a 'd'
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

\begin{bnf*}
    \bnfprod{a}{\bnfpn{a} \bnfsp \bnfpn{b}}
    \bnfprod{b}{\bnftd{[} \bnfpn{b}\bnftd{]} \bnfsp \bnfpn{c}}\\
    \bnfmore{\bnfor \bnftd{[} \bnfpn{b}\bnftd{]} \bnfsp \bnfpn{c}}\\
    \bnfmore{\bnfor \bnfpn{a} \bnfsp \bnfts{d}}\\
    \bnfmore{\bnfor \bnfts{$\alpha$}}\\
    \bnfprod{op}{\bnfts{+} \bnfor \bnfts{-} \bnfor \bnfts{*}}
\end{bnf*}
``` 
 

