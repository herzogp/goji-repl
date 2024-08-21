# New Syntax

y1 # value of y1 in current Env
'abc' # value
206 # value
46.89 # value
#t # value
#f # value

ident = expr


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


