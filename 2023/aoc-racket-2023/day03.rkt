#lang racket

(require "utils.rkt")

(provide number symbol neighborhood adjacent? part-numbers parse)

(struct number (value pos) #:transparent)
(struct symbol (value pos) #:transparent)

(define (neighborhood sym)
  (let ([relatives (cartesian-product '(-1 0 1) '(-1 0 1))])
       (map
        (lambda (x) (list-+ (symbol-pos sym) x))
        relatives)))

(define (adjacent? num sym)
  (> (length (set-intersect (neighborhood sym) (number-pos num))) 0))

(define (any? l)
  (foldl (lambda (x y) (or x y)) #f l))

(define (part-numbers lnums lsyms)
  (filter
    (lambda (num) (any? (map
                          (lambda (sym) (adjacent? num sym))
                          lsyms)))
    lnums))

(define (symbol-token? t)
  (cond
    [(char-numeric? t) #f]
    [(eq? t #\.) #f]
    [else #t]))

(define (parse input)
  (let ([tokens (tokenize input)])
       (list
        '()
        (map (lambda (x) (symbol (second x) (first x))) (filter (compose symbol-token? second) tokens)))))

(define (tokenize input)
  ((compose
    (curry apply append)
    (curry map
      (lambda (row) (map (lambda (el) (list (list (first row) (first el)) (second el)))
                         (second row))))
    enumerate
    (curry map
      (compose
        enumerate
        string->list)))
    (string-split input "\n")))
