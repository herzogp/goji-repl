; define a few functions
(define (x1 a b) (+ a b))
(define (x2 b) (* b b))

; Now invoke these functions
(  x1 "abc"  7   'xyz'   )
(x2 (x1 40.1 52))

; Done
