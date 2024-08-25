// define a few functions
(= (x1 a b) (+ a b))
(= (x2 b) (* b b))

// Now invoke these functions
(  x1 "abc"  7   'xyz'   )
(x2 (x1 40.1 52))

// Done
