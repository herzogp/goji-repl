# New Syntax

y1 # value of y1 in current Env
'abc' # value
206 # value
46.89 # value
#t # value
#f # value

ident = expr

expressions (expr)
==================
VALUE ::= 
       | INTEGER 
       | FLOAT 
       | BOOL 
       | TEXT

BINARY_OP ::= '+' | '*' | '<' | '>' | '&' | '|'
ASSIGN_OP ::= '='
UNARY_OP ::= '!'

LIST_BEGIN ::= '('
LIST_END ::= ')'

EXPR ::= 
      | VALUE 
      | IDENT
      | IDENT ASSIGN_OP EXPR
      | LIST_BEGIN EXPR LIST_END
      | EXPR BINARY_OP EXPR
      | UNARY_OP EXPR

fn a1 a2 {
  // body ...
}

count1 a1 a2 = {
  // body ...
}

Some ideas 
----------
ITEM ::= IDENT

ITERATOR ::= IDENT

each ITEM IN_ ITERATOR BLOCK

; every iterable can be used as a 
function (via call()) which evaluates a block
for each named item delivered by the iterable
and the block can also exit early

; if all_plants is a list (which supports iterable)
then it can be 'iterated' like this:


all_plants(p) {
    exit when p.hasColor('red')
    print p 
}

fn_name arg1 arg2 ...

fn name param1, param2, ... -> 
  let
   v1 = expr using zero or more params
   v2 = expr...
  in 
   expr using params and locals

sq3 = 4

sq4 a1:int a2:int -> 
let 
  v1 = a1 + 20
  v2 = 19
in
  v1 * a2


const sq4 = (a1, a2) => {

  const v1 = a1 + 20
  const v2 = 19

  return v1 * a2
}


