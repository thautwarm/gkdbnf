
"""
Copyright thautwarm (c) 2019

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

    * Neither the name of thautwarm nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from dataclasses import dataclass
from typing import *
@dataclass
class Term:
     v: str

@dataclass
class NonTerm:
     v: str

@dataclass
class Or:
     pass

@dataclass
class Seq:
     xs: 'List[Union[NonTerm, Term, Or]]'
     label: str
     
@dataclass
class More:
     impl: Seq


@dataclass
class Prod:
     descr: str
     name: str
     type: str
     impl : Seq

DEF = r'\bnfdef'
TYPEOF = r'\bnfistypeof'
TYPE = r'\bnftype'
OR = r'\bnfalt'
NT = r'\bnfnonterm'
SPACE = r' \bnfspace '
TERM = r'\bnfterm'
DESCR = r'\bnfdescr'
LABEL = r'\bnflabel'
MKLINE = '\\\\\n'

def macro_apply(macro, *args):
     res = macro
     for arg in args:
          res = f'{res}{{ {arg} }}'
     return res

xor = Term("|")
eq = Term("=")
define = Term("::=")
ann = Term("::")

join = MKLINE.join
def unwrap(x): return x[1:-1]

def to_latex(xs):
     from io import StringIO
     xs = iter(xs)
     lastlineno, x = next(xs)
     io = StringIO()
     print = io.write
     to_backnaur(print, x)
     for lineno, x in xs:
          print('\n')
          print((lineno - lastlineno - 1) * MKLINE)
          to_backnaur(print, x)
     return io.getvalue()

def to_backnaur(print, x):

     if isinstance(x, Prod):
          if x.descr:
               print(macro_apply(DESCR, x.descr))
               print(macro_apply(SPACE))

          print(' & ')

          to_backnaur(print, NonTerm(x.name))

          if x.type:
               print(' & ')
               print(macro_apply(TYPEOF))
               print(' & ')
               print(macro_apply(TYPE, x.type))
               print(' & ')
          else:
               print(' & & & ')
          
          print(macro_apply(DEF))
          print(' & ')

          to_backnaur(print, x.impl)
          return
     if isinstance(x, Term):
          return print(macro_apply(TERM, x.v))
     if isinstance(x, NonTerm):
          return print(macro_apply(NT,  x.v))
     if isinstance(x, Or):
          print(macro_apply(OR))
     if isinstance(x, More):
          # desc
          print(' & ')
          # name
          print(' & ')
          # typeof
          print(' & ')
          # type
          print(' & ')
          print(macro_apply(OR))
          print(' & ')
          return to_backnaur(print, x.impl)
     if isinstance(x, Seq):
          if not x.xs:
               print(' & ')
               return
          print(" $ ")
          xs = iter(x.xs)
          to_backnaur(print, next(xs))
          for e in x.xs:
               print(macro_apply(SPACE))
               to_backnaur(print, e)
          
          print(" $ ")
          print(' & ')
          if x.label:
               print(macro_apply(LABEL, x.label))
          return
from typing import Generic, TypeVar
T = TypeVar('T')

class Tokens():
    __slots__ = ['array', 'offset']

    def __init__(self, array):
        self.array = array
        self.offset = 0

class State():

    def __init__(self):
        pass

class AST(Generic[T]):
    __slots__ = ['tag', 'contents']

    def __init__(self, tag: str, contents: T):
        self.tag = tag
        self.contents = contents

class Nil():
    nil = None
    __slots__ = []

    def __init__(self):
        if (Nil.nil is None):
            Nil.nil = self
            return
        raise ValueError('Nil cannot get instantiated twice.')

    def __len__(self):
        return 0

    def __getitem__(self, n):
        raise IndexError('Out of bounds')

    @property
    def head(self):
        raise IndexError('Out of bounds')

    @property
    def tail(self):
        raise IndexError('Out of bounds')

    def __repr__(self):
        return '[]'
_nil = Nil()

class Cons():
    __slots__ = ['head', 'tail']

    def __init__(self, _head, _tail):
        self.head = _head
        self.tail = _tail

    def __len__(self):
        nil = _nil
        l = 0
        while (self is not nil):
            l += 1
            self = self.tail
        return l

    def __iter__(self):
        nil = _nil
        while (self is not nil):
            (yield self.head)
            self = self.tail

    def __getitem__(self, n):
        while (n != 0):
            self = self.tail
            n -= 1
        return self.head

    def __repr__(self):
        return repr(list(self))
try:

    def mk_pretty():
        from prettyprinter import register_pretty, pretty_call, pprint

        @register_pretty(Tokens)
        def pretty_tokens(value, ctx):
            return pretty_call(ctx, Tokens, offset=value.offset, array=value.array)

        @register_pretty(AST)
        def pretty_ast(value, ctx):
            return pretty_call(ctx, AST, tag=value.tag, contents=value.contents)
    mk_pretty()
    del mk_pretty
except ImportError:
    pass
del T, Generic, TypeVar
builtin_cons = Cons
builtin_nil = _nil
builtin_mk_ast = AST

def mk_parser():
    pass

    def rbnf_named_lr_step_prod(rbnf_tmp_0, builtin_state, builtin_tokens):
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        try:
            builtin_tokens.array[(builtin_tokens.offset + 0)]
            _rbnf_peek_tmp = True
        except IndexError:
            _rbnf_peek_tmp = False
        lcl_0 = _rbnf_peek_tmp
        if lcl_0:
            lcl_2 = builtin_tokens.array[(builtin_tokens.offset + 0)]
            lcl_2 = lcl_2.idint
            if (lcl_2 == 8):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_1 = lcl_3
                lcl_3 = builtin_tokens.offset
                rbnf_named__off_1 = lcl_3
                try:
                    builtin_tokens.array[(builtin_tokens.offset + 0)]
                    _rbnf_peek_tmp = True
                except IndexError:
                    _rbnf_peek_tmp = False
                lcl_3 = _rbnf_peek_tmp
                if lcl_3:
                    lcl_5 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                    lcl_5 = lcl_5.idint
                    if (lcl_5 == 3):
                        lcl_6 = rbnf_named_parse_singleprod(builtin_state, builtin_tokens)
                        rbnf_named__check_2 = lcl_6
                        lcl_6 = rbnf_named__check_2[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_2
                        else:
                            lcl_7 = rbnf_named__check_2[1]
                            rbnf_tmp_2 = lcl_7
                            lcl_7 = rbnf_tmp_0.append
                            lcl_7 = lcl_7(rbnf_tmp_2)
                            rbnf_tmp_1_ = rbnf_tmp_0
                            lcl_8 = (True, rbnf_tmp_1_)
                            lcl_6 = lcl_8
                        lcl_4 = lcl_6
                    elif (lcl_5 == 2):
                        lcl_6 = rbnf_named_parse_singleprod(builtin_state, builtin_tokens)
                        rbnf_named__check_2 = lcl_6
                        lcl_6 = rbnf_named__check_2[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_2
                        else:
                            lcl_8 = rbnf_named__check_2[1]
                            rbnf_tmp_2 = lcl_8
                            lcl_8 = rbnf_tmp_0.append
                            lcl_8 = lcl_8(rbnf_tmp_2)
                            rbnf_tmp_1_ = rbnf_tmp_0
                            lcl_9 = (True, rbnf_tmp_1_)
                            lcl_6 = lcl_9
                        lcl_4 = lcl_6
                    elif (lcl_5 == 1):
                        lcl_6 = rbnf_named_parse_singleprod(builtin_state, builtin_tokens)
                        rbnf_named__check_2 = lcl_6
                        lcl_6 = rbnf_named__check_2[0]
                        lcl_6 = (lcl_6 == False)
                        if lcl_6:
                            lcl_6 = rbnf_named__check_2
                        else:
                            lcl_9 = rbnf_named__check_2[1]
                            rbnf_tmp_2 = lcl_9
                            lcl_9 = rbnf_tmp_0.append
                            lcl_9 = lcl_9(rbnf_tmp_2)
                            rbnf_tmp_1_ = rbnf_tmp_0
                            lcl_10 = (True, rbnf_tmp_1_)
                            lcl_6 = lcl_10
                        lcl_4 = lcl_6
                    elif (lcl_5 == 0):
                        lcl_10 = rbnf_named_parse_singleprod(builtin_state, builtin_tokens)
                        rbnf_named__check_2 = lcl_10
                        lcl_10 = rbnf_named__check_2[0]
                        lcl_10 = (lcl_10 == False)
                        if lcl_10:
                            lcl_10 = rbnf_named__check_2
                        else:
                            lcl_6 = rbnf_named__check_2[1]
                            rbnf_tmp_2 = lcl_6
                            lcl_6 = rbnf_tmp_0.append
                            lcl_6 = lcl_6(rbnf_tmp_2)
                            rbnf_tmp_1_ = rbnf_tmp_0
                            lcl_11 = (True, rbnf_tmp_1_)
                            lcl_10 = lcl_11
                        lcl_4 = lcl_10
                    elif (lcl_5 == 8):
                        rbnf_tmp_1_ = rbnf_tmp_0
                        lcl_10 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_10
                    elif (lcl_5 == 9):
                        rbnf_tmp_1_ = rbnf_tmp_0
                        lcl_10 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_10
                    else:
                        rbnf_tmp_1_ = rbnf_tmp_0
                        lcl_10 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_10
                    lcl_3 = lcl_4
                else:
                    lcl_10 = (rbnf_named__off_1, 'prod got EOF')
                    lcl_10 = builtin_cons(lcl_10, builtin_nil)
                    lcl_10 = (False, lcl_10)
                    lcl_3 = lcl_10
                lcl_1 = lcl_3
            elif (lcl_2 == 9):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_10 = _rbnf_cur_token
                rbnf_tmp_1 = lcl_10
                rbnf_tmp_1_ = rbnf_tmp_0
                lcl_10 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_10
            else:
                lcl_10 = (rbnf_named__off_0, 'prod lookahead failed')
                lcl_10 = builtin_cons(lcl_10, builtin_nil)
                lcl_10 = (False, lcl_10)
                lcl_1 = lcl_10
            lcl_0 = lcl_1
        else:
            lcl_1 = (rbnf_named__off_0, 'prod got EOF')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_lr_loop_prod(rbnf_tmp_0, builtin_state, builtin_tokens):
        rbnf_named_lr_prod_reduce = rbnf_tmp_0
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        lcl_0 = rbnf_named_lr_step_prod(rbnf_named_lr_prod_reduce, builtin_state, builtin_tokens)
        rbnf_named_lr_prod_try = lcl_0
        lcl_0 = rbnf_named_lr_prod_try[0]
        lcl_0 = (lcl_0 is not False)
        while lcl_0:
            lcl_1 = builtin_tokens.offset
            rbnf_named__off_0 = lcl_1
            lcl_1 = rbnf_named_lr_prod_try[1]
            rbnf_named_lr_prod_reduce = lcl_1
            lcl_1 = rbnf_named_lr_step_prod(rbnf_named_lr_prod_reduce, builtin_state, builtin_tokens)
            rbnf_named_lr_prod_try = lcl_1
            lcl_1 = rbnf_named_lr_prod_try[0]
            lcl_1 = (lcl_1 is not False)
            lcl_0 = lcl_1
        lcl_0 = builtin_tokens.offset
        lcl_0 = (lcl_0 == rbnf_named__off_0)
        if lcl_0:
            lcl_1 = (True, rbnf_named_lr_prod_reduce)
            lcl_0 = lcl_1
        else:
            lcl_0 = rbnf_named_lr_prod_try
        return lcl_0

    def rbnf_named_lr_step_rbnfmacro_0(rbnf_tmp_0, builtin_state, builtin_tokens):
        lcl_0 = rbnf_named_parse_atom(builtin_state, builtin_tokens)
        rbnf_named__check_1 = lcl_0
        lcl_0 = rbnf_named__check_1[0]
        lcl_0 = (lcl_0 == False)
        if lcl_0:
            lcl_0 = rbnf_named__check_1
        else:
            lcl_1 = rbnf_named__check_1[1]
            rbnf_tmp_1 = lcl_1
            lcl_1 = rbnf_tmp_0.append
            lcl_1 = lcl_1(rbnf_tmp_1)
            rbnf_tmp_1_ = rbnf_tmp_0
            lcl_2 = (True, rbnf_tmp_1_)
            lcl_0 = lcl_2
        return lcl_0

    def rbnf_named_lr_loop_rbnfmacro_0(rbnf_tmp_0, builtin_state, builtin_tokens):
        rbnf_named_lr_rbnfmacro_0_reduce = rbnf_tmp_0
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        lcl_0 = rbnf_named_lr_step_rbnfmacro_0(rbnf_named_lr_rbnfmacro_0_reduce, builtin_state, builtin_tokens)
        rbnf_named_lr_rbnfmacro_0_try = lcl_0
        lcl_0 = rbnf_named_lr_rbnfmacro_0_try[0]
        lcl_0 = (lcl_0 is not False)
        while lcl_0:
            lcl_1 = builtin_tokens.offset
            rbnf_named__off_0 = lcl_1
            lcl_1 = rbnf_named_lr_rbnfmacro_0_try[1]
            rbnf_named_lr_rbnfmacro_0_reduce = lcl_1
            lcl_1 = rbnf_named_lr_step_rbnfmacro_0(rbnf_named_lr_rbnfmacro_0_reduce, builtin_state, builtin_tokens)
            rbnf_named_lr_rbnfmacro_0_try = lcl_1
            lcl_1 = rbnf_named_lr_rbnfmacro_0_try[0]
            lcl_1 = (lcl_1 is not False)
            lcl_0 = lcl_1
        lcl_0 = builtin_tokens.offset
        lcl_0 = (lcl_0 == rbnf_named__off_0)
        if lcl_0:
            lcl_1 = (True, rbnf_named_lr_rbnfmacro_0_reduce)
            lcl_0 = lcl_1
        else:
            lcl_0 = rbnf_named_lr_rbnfmacro_0_try
        return lcl_0

    def rbnf_named_parse_START(builtin_state, builtin_tokens):
        try:
            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
            if (_rbnf_cur_token.idint is 10):
                builtin_tokens.offset += 1
            else:
                _rbnf_cur_token = None
        except IndexError:
            _rbnf_cur_token = None
        lcl_0 = _rbnf_cur_token
        rbnf_tmp_0 = lcl_0
        lcl_0 = (rbnf_tmp_0 is None)
        if lcl_0:
            lcl_1 = builtin_tokens.offset
            lcl_1 = (lcl_1, 'BOF not match')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        else:
            lcl_1 = builtin_tokens.offset
            rbnf_named__off_1 = lcl_1
            try:
                builtin_tokens.array[(builtin_tokens.offset + 0)]
                _rbnf_peek_tmp = True
            except IndexError:
                _rbnf_peek_tmp = False
            lcl_1 = _rbnf_peek_tmp
            if lcl_1:
                lcl_3 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                lcl_3 = lcl_3.idint
                if (lcl_3 == 3):
                    lcl_4 = rbnf_named_parse_prod(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_4
                    lcl_4 = rbnf_named__check_1[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_1
                    else:
                        lcl_5 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_5
                        lcl_5 = to_latex(rbnf_tmp_1)
                        rbnf_tmp_1_ = lcl_5
                        lcl_5 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_5
                    lcl_2 = lcl_4
                elif (lcl_3 == 2):
                    lcl_4 = rbnf_named_parse_prod(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_4
                    lcl_4 = rbnf_named__check_1[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_1
                    else:
                        lcl_5 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_5
                        lcl_5 = to_latex(rbnf_tmp_1)
                        rbnf_tmp_1_ = lcl_5
                        lcl_5 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_5
                    lcl_2 = lcl_4
                elif (lcl_3 == 1):
                    lcl_4 = rbnf_named_parse_prod(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_4
                    lcl_4 = rbnf_named__check_1[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_1
                    else:
                        lcl_5 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_5
                        lcl_5 = to_latex(rbnf_tmp_1)
                        rbnf_tmp_1_ = lcl_5
                        lcl_5 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_5
                    lcl_2 = lcl_4
                elif (lcl_3 == 0):
                    lcl_4 = rbnf_named_parse_prod(builtin_state, builtin_tokens)
                    rbnf_named__check_1 = lcl_4
                    lcl_4 = rbnf_named__check_1[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_1
                    else:
                        lcl_5 = rbnf_named__check_1[1]
                        rbnf_tmp_1 = lcl_5
                        lcl_5 = to_latex(rbnf_tmp_1)
                        rbnf_tmp_1_ = lcl_5
                        lcl_5 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_5
                    lcl_2 = lcl_4
                elif (lcl_3 == 8):
                    _rbnf_old_offset = builtin_tokens.offset
                    _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                    builtin_tokens.offset = (_rbnf_old_offset + 1)
                    lcl_4 = _rbnf_cur_token
                    rbnf_tmp_1 = lcl_4
                    lcl_4 = rbnf_named_parse_prod(builtin_state, builtin_tokens)
                    rbnf_named__check_2 = lcl_4
                    lcl_4 = rbnf_named__check_2[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_2
                    else:
                        lcl_5 = rbnf_named__check_2[1]
                        rbnf_tmp_2 = lcl_5
                        lcl_5 = to_latex(rbnf_tmp_2)
                        rbnf_tmp_1_ = lcl_5
                        lcl_5 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_5
                    lcl_2 = lcl_4
                else:
                    lcl_4 = (rbnf_named__off_1, 'START lookahead failed')
                    lcl_4 = builtin_cons(lcl_4, builtin_nil)
                    lcl_4 = (False, lcl_4)
                    lcl_2 = lcl_4
                lcl_1 = lcl_2
            else:
                lcl_2 = (rbnf_named__off_1, 'START got EOF')
                lcl_2 = builtin_cons(lcl_2, builtin_nil)
                lcl_2 = (False, lcl_2)
                lcl_1 = lcl_2
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_atom(builtin_state, builtin_tokens):
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        try:
            builtin_tokens.array[(builtin_tokens.offset + 0)]
            _rbnf_peek_tmp = True
        except IndexError:
            _rbnf_peek_tmp = False
        lcl_0 = _rbnf_peek_tmp
        if lcl_0:
            lcl_2 = builtin_tokens.array[(builtin_tokens.offset + 0)]
            lcl_2 = lcl_2.idint
            if (lcl_2 == 3):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = Or()
                rbnf_tmp_1_ = lcl_3
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            elif (lcl_2 == 4):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                rbnf_tmp_1_ = eq
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            elif (lcl_2 == 6):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                rbnf_tmp_1_ = define
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            elif (lcl_2 == 5):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                rbnf_tmp_1_ = ann
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            elif (lcl_2 == 2):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_tmp_0.value
                lcl_3 = unwrap(lcl_3)
                lcl_3 = Term(lcl_3)
                rbnf_tmp_1_ = lcl_3
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            elif (lcl_2 == 1):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_tmp_0.value
                lcl_3 = Term(lcl_3)
                rbnf_tmp_1_ = lcl_3
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            elif (lcl_2 == 0):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_tmp_0.value
                lcl_3 = unwrap(lcl_3)
                lcl_3 = NonTerm(lcl_3)
                rbnf_tmp_1_ = lcl_3
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            else:
                lcl_3 = (rbnf_named__off_0, 'atom lookahead failed')
                lcl_3 = builtin_cons(lcl_3, builtin_nil)
                lcl_3 = (False, lcl_3)
                lcl_1 = lcl_3
            lcl_0 = lcl_1
        else:
            lcl_1 = (rbnf_named__off_0, 'atom got EOF')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_prod(builtin_state, builtin_tokens):
        lcl_0 = rbnf_named_parse_singleprod(builtin_state, builtin_tokens)
        rbnf_named__check_0 = lcl_0
        lcl_0 = rbnf_named__check_0[0]
        lcl_0 = (lcl_0 == False)
        if lcl_0:
            lcl_0 = rbnf_named__check_0
        else:
            lcl_1 = rbnf_named__check_0[1]
            rbnf_tmp_0 = lcl_1
            lcl_1 = []
            _rbnf_immediate_lst = lcl_1
            _rbnf_immediate_lst.append(rbnf_tmp_0)
            lcl_1 = _rbnf_immediate_lst
            rbnf_tmp_1_ = lcl_1
            lcl_1 = rbnf_named_lr_loop_prod(rbnf_tmp_1_, builtin_state, builtin_tokens)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_rbnfmacro_0(builtin_state, builtin_tokens):
        lcl_0 = rbnf_named_parse_atom(builtin_state, builtin_tokens)
        rbnf_named__check_0 = lcl_0
        lcl_0 = rbnf_named__check_0[0]
        lcl_0 = (lcl_0 == False)
        if lcl_0:
            lcl_0 = rbnf_named__check_0
        else:
            lcl_1 = rbnf_named__check_0[1]
            rbnf_tmp_0 = lcl_1
            lcl_1 = []
            _rbnf_immediate_lst = lcl_1
            _rbnf_immediate_lst.append(rbnf_tmp_0)
            lcl_1 = _rbnf_immediate_lst
            rbnf_tmp_1_ = lcl_1
            lcl_1 = rbnf_named_lr_loop_rbnfmacro_0(rbnf_tmp_1_, builtin_state, builtin_tokens)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_rule(builtin_state, builtin_tokens):
        lcl_0 = rbnf_named_parse_rbnfmacro_0(builtin_state, builtin_tokens)
        rbnf_named__check_0 = lcl_0
        lcl_0 = rbnf_named__check_0[0]
        lcl_0 = (lcl_0 == False)
        if lcl_0:
            lcl_0 = rbnf_named__check_0
        else:
            lcl_1 = rbnf_named__check_0[1]
            rbnf_tmp_0 = lcl_1
            lcl_1 = builtin_tokens.offset
            rbnf_named__off_0 = lcl_1
            try:
                builtin_tokens.array[(builtin_tokens.offset + 0)]
                _rbnf_peek_tmp = True
            except IndexError:
                _rbnf_peek_tmp = False
            lcl_1 = _rbnf_peek_tmp
            if lcl_1:
                lcl_3 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                lcl_3 = lcl_3.idint
                if (lcl_3 == 7):
                    _rbnf_old_offset = builtin_tokens.offset
                    _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                    builtin_tokens.offset = (_rbnf_old_offset + 1)
                    lcl_4 = _rbnf_cur_token
                    rbnf_tmp_1 = lcl_4
                    try:
                        _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                        if (_rbnf_cur_token.idint is 2):
                            builtin_tokens.offset += 1
                        else:
                            _rbnf_cur_token = None
                    except IndexError:
                        _rbnf_cur_token = None
                    lcl_4 = _rbnf_cur_token
                    rbnf_tmp_2 = lcl_4
                    lcl_4 = (rbnf_tmp_2 is None)
                    if lcl_4:
                        lcl_5 = builtin_tokens.offset
                        lcl_5 = (lcl_5, 'Term2 not match')
                        lcl_5 = builtin_cons(lcl_5, builtin_nil)
                        lcl_5 = (False, lcl_5)
                        lcl_4 = lcl_5
                    else:
                        lcl_5 = rbnf_tmp_2.value
                        lcl_5 = Seq(rbnf_tmp_0, lcl_5)
                        rbnf_tmp_1_ = lcl_5
                        lcl_5 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_5
                    lcl_2 = lcl_4
                else:
                    lcl_4 = Seq(rbnf_tmp_0, None)
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = (True, rbnf_tmp_1_)
                    lcl_2 = lcl_4
                lcl_1 = lcl_2
            else:
                lcl_2 = (rbnf_named__off_0, 'rule got EOF')
                lcl_2 = builtin_cons(lcl_2, builtin_nil)
                lcl_2 = (False, lcl_2)
                lcl_1 = lcl_2
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_singleprod(builtin_state, builtin_tokens):
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        try:
            builtin_tokens.array[(builtin_tokens.offset + 0)]
            _rbnf_peek_tmp = True
        except IndexError:
            _rbnf_peek_tmp = False
        lcl_0 = _rbnf_peek_tmp
        if lcl_0:
            lcl_2 = builtin_tokens.array[(builtin_tokens.offset + 0)]
            lcl_2 = lcl_2.idint
            if (lcl_2 == 3):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_named_parse_rule(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_3
                lcl_3 = rbnf_named__check_1[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_1
                else:
                    lcl_4 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_4
                    lcl_4 = rbnf_tmp_0.lineno
                    lcl_5 = More(rbnf_tmp_1)
                    lcl_4 = (lcl_4, lcl_5)
                    rbnf_tmp_1_ = lcl_4
                    lcl_4 = (True, rbnf_tmp_1_)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 2):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                try:
                    _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                    if (_rbnf_cur_token.idint is 0):
                        builtin_tokens.offset += 1
                    else:
                        _rbnf_cur_token = None
                except IndexError:
                    _rbnf_cur_token = None
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_1 = lcl_3
                lcl_3 = (rbnf_tmp_1 is None)
                if lcl_3:
                    lcl_4 = builtin_tokens.offset
                    lcl_4 = (lcl_4, 'NonTerm not match')
                    lcl_4 = builtin_cons(lcl_4, builtin_nil)
                    lcl_4 = (False, lcl_4)
                    lcl_3 = lcl_4
                else:
                    lcl_4 = rbnf_named_parse_type(builtin_state, builtin_tokens)
                    rbnf_named__check_2 = lcl_4
                    lcl_4 = rbnf_named__check_2[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_2
                    else:
                        lcl_5 = rbnf_named__check_2[1]
                        rbnf_tmp_2 = lcl_5
                        lcl_5 = rbnf_named_parse_rule(builtin_state, builtin_tokens)
                        rbnf_named__check_3 = lcl_5
                        lcl_5 = rbnf_named__check_3[0]
                        lcl_5 = (lcl_5 == False)
                        if lcl_5:
                            lcl_5 = rbnf_named__check_3
                        else:
                            lcl_6 = rbnf_named__check_3[1]
                            rbnf_tmp_3 = lcl_6
                            lcl_6 = rbnf_tmp_0.lineno
                            lcl_7 = rbnf_tmp_0.value
                            lcl_7 = unwrap(lcl_7)
                            lcl_8 = rbnf_tmp_1.value
                            lcl_8 = unwrap(lcl_8)
                            lcl_7 = Prod(lcl_7, lcl_8, rbnf_tmp_2, rbnf_tmp_3)
                            lcl_6 = (lcl_6, lcl_7)
                            rbnf_tmp_1_ = lcl_6
                            lcl_6 = (True, rbnf_tmp_1_)
                            lcl_5 = lcl_6
                        lcl_4 = lcl_5
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 1):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                try:
                    _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                    if (_rbnf_cur_token.idint is 0):
                        builtin_tokens.offset += 1
                    else:
                        _rbnf_cur_token = None
                except IndexError:
                    _rbnf_cur_token = None
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_1 = lcl_3
                lcl_3 = (rbnf_tmp_1 is None)
                if lcl_3:
                    lcl_4 = builtin_tokens.offset
                    lcl_4 = (lcl_4, 'NonTerm not match')
                    lcl_4 = builtin_cons(lcl_4, builtin_nil)
                    lcl_4 = (False, lcl_4)
                    lcl_3 = lcl_4
                else:
                    lcl_4 = rbnf_named_parse_type(builtin_state, builtin_tokens)
                    rbnf_named__check_2 = lcl_4
                    lcl_4 = rbnf_named__check_2[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_2
                    else:
                        lcl_5 = rbnf_named__check_2[1]
                        rbnf_tmp_2 = lcl_5
                        lcl_5 = rbnf_named_parse_rule(builtin_state, builtin_tokens)
                        rbnf_named__check_3 = lcl_5
                        lcl_5 = rbnf_named__check_3[0]
                        lcl_5 = (lcl_5 == False)
                        if lcl_5:
                            lcl_5 = rbnf_named__check_3
                        else:
                            lcl_6 = rbnf_named__check_3[1]
                            rbnf_tmp_3 = lcl_6
                            lcl_6 = rbnf_tmp_0.lineno
                            lcl_7 = rbnf_tmp_0.value
                            lcl_8 = rbnf_tmp_1.value
                            lcl_8 = unwrap(lcl_8)
                            lcl_7 = Prod(lcl_7, lcl_8, rbnf_tmp_2, rbnf_tmp_3)
                            lcl_6 = (lcl_6, lcl_7)
                            rbnf_tmp_1_ = lcl_6
                            lcl_6 = (True, rbnf_tmp_1_)
                            lcl_5 = lcl_6
                        lcl_4 = lcl_5
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            elif (lcl_2 == 0):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = rbnf_named_parse_type(builtin_state, builtin_tokens)
                rbnf_named__check_1 = lcl_3
                lcl_3 = rbnf_named__check_1[0]
                lcl_3 = (lcl_3 == False)
                if lcl_3:
                    lcl_3 = rbnf_named__check_1
                else:
                    lcl_4 = rbnf_named__check_1[1]
                    rbnf_tmp_1 = lcl_4
                    lcl_4 = rbnf_named_parse_rule(builtin_state, builtin_tokens)
                    rbnf_named__check_2 = lcl_4
                    lcl_4 = rbnf_named__check_2[0]
                    lcl_4 = (lcl_4 == False)
                    if lcl_4:
                        lcl_4 = rbnf_named__check_2
                    else:
                        lcl_5 = rbnf_named__check_2[1]
                        rbnf_tmp_2 = lcl_5
                        lcl_5 = rbnf_tmp_0.lineno
                        lcl_6 = rbnf_tmp_0.value
                        lcl_6 = unwrap(lcl_6)
                        lcl_6 = Prod(None, lcl_6, rbnf_tmp_1, rbnf_tmp_2)
                        lcl_5 = (lcl_5, lcl_6)
                        rbnf_tmp_1_ = lcl_5
                        lcl_5 = (True, rbnf_tmp_1_)
                        lcl_4 = lcl_5
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            else:
                lcl_3 = (rbnf_named__off_0, 'singleprod lookahead failed')
                lcl_3 = builtin_cons(lcl_3, builtin_nil)
                lcl_3 = (False, lcl_3)
                lcl_1 = lcl_3
            lcl_0 = lcl_1
        else:
            lcl_1 = (rbnf_named__off_0, 'singleprod got EOF')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        return lcl_0

    def rbnf_named_parse_type(builtin_state, builtin_tokens):
        lcl_0 = builtin_tokens.offset
        rbnf_named__off_0 = lcl_0
        try:
            builtin_tokens.array[(builtin_tokens.offset + 0)]
            _rbnf_peek_tmp = True
        except IndexError:
            _rbnf_peek_tmp = False
        lcl_0 = _rbnf_peek_tmp
        if lcl_0:
            lcl_2 = builtin_tokens.array[(builtin_tokens.offset + 0)]
            lcl_2 = lcl_2.idint
            if (lcl_2 == 6):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                rbnf_tmp_1_ = None
                lcl_3 = (True, rbnf_tmp_1_)
                lcl_1 = lcl_3
            elif (lcl_2 == 5):
                _rbnf_old_offset = builtin_tokens.offset
                _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                builtin_tokens.offset = (_rbnf_old_offset + 1)
                lcl_3 = _rbnf_cur_token
                rbnf_tmp_0 = lcl_3
                lcl_3 = builtin_tokens.offset
                rbnf_named__off_1 = lcl_3
                try:
                    builtin_tokens.array[(builtin_tokens.offset + 0)]
                    _rbnf_peek_tmp = True
                except IndexError:
                    _rbnf_peek_tmp = False
                lcl_3 = _rbnf_peek_tmp
                if lcl_3:
                    lcl_5 = builtin_tokens.array[(builtin_tokens.offset + 0)]
                    lcl_5 = lcl_5.idint
                    if (lcl_5 == 2):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 4):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_6
                        lcl_6 = (rbnf_tmp_2 is None)
                        if lcl_6:
                            lcl_7 = builtin_tokens.offset
                            lcl_7 = (lcl_7, 'quote = not match')
                            lcl_7 = builtin_cons(lcl_7, builtin_nil)
                            lcl_7 = (False, lcl_7)
                            lcl_6 = lcl_7
                        else:
                            lcl_7 = rbnf_tmp_1.value
                            lcl_7 = unwrap(lcl_7)
                            rbnf_tmp_1_ = lcl_7
                            lcl_7 = (True, rbnf_tmp_1_)
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    elif (lcl_5 == 1):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 4):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_6
                        lcl_6 = (rbnf_tmp_2 is None)
                        if lcl_6:
                            lcl_7 = builtin_tokens.offset
                            lcl_7 = (lcl_7, 'quote = not match')
                            lcl_7 = builtin_cons(lcl_7, builtin_nil)
                            lcl_7 = (False, lcl_7)
                            lcl_6 = lcl_7
                        else:
                            lcl_7 = rbnf_tmp_1.value
                            rbnf_tmp_1_ = lcl_7
                            lcl_7 = (True, rbnf_tmp_1_)
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    elif (lcl_5 == 0):
                        _rbnf_old_offset = builtin_tokens.offset
                        _rbnf_cur_token = builtin_tokens.array[_rbnf_old_offset]
                        builtin_tokens.offset = (_rbnf_old_offset + 1)
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_1 = lcl_6
                        try:
                            _rbnf_cur_token = builtin_tokens.array[builtin_tokens.offset]
                            if (_rbnf_cur_token.idint is 4):
                                builtin_tokens.offset += 1
                            else:
                                _rbnf_cur_token = None
                        except IndexError:
                            _rbnf_cur_token = None
                        lcl_6 = _rbnf_cur_token
                        rbnf_tmp_2 = lcl_6
                        lcl_6 = (rbnf_tmp_2 is None)
                        if lcl_6:
                            lcl_7 = builtin_tokens.offset
                            lcl_7 = (lcl_7, 'quote = not match')
                            lcl_7 = builtin_cons(lcl_7, builtin_nil)
                            lcl_7 = (False, lcl_7)
                            lcl_6 = lcl_7
                        else:
                            lcl_7 = rbnf_tmp_1.value
                            lcl_7 = unwrap(lcl_7)
                            rbnf_tmp_1_ = lcl_7
                            lcl_7 = (True, rbnf_tmp_1_)
                            lcl_6 = lcl_7
                        lcl_4 = lcl_6
                    else:
                        lcl_6 = (rbnf_named__off_1, 'type lookahead failed')
                        lcl_6 = builtin_cons(lcl_6, builtin_nil)
                        lcl_6 = (False, lcl_6)
                        lcl_4 = lcl_6
                    lcl_3 = lcl_4
                else:
                    lcl_4 = (rbnf_named__off_1, 'type got EOF')
                    lcl_4 = builtin_cons(lcl_4, builtin_nil)
                    lcl_4 = (False, lcl_4)
                    lcl_3 = lcl_4
                lcl_1 = lcl_3
            else:
                lcl_3 = (rbnf_named__off_0, 'type lookahead failed')
                lcl_3 = builtin_cons(lcl_3, builtin_nil)
                lcl_3 = (False, lcl_3)
                lcl_1 = lcl_3
            lcl_0 = lcl_1
        else:
            lcl_1 = (rbnf_named__off_0, 'type got EOF')
            lcl_1 = builtin_cons(lcl_1, builtin_nil)
            lcl_1 = (False, lcl_1)
            lcl_0 = lcl_1
        return lcl_0
    return rbnf_named_parse_START