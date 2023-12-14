#lang racket

(provide ones zip enumerate list-+ list-scalar-*)

(define (ones n)
  (build-list n (lambda (_) 1)))

(define (zip l1 l2)
  (if (empty? l1)
      '()
      (cons (list (first l1) (first l2)) (zip (rest l1) (rest l2)))))

(define (enumerate l)
  (zip (range (length l)) l))

(define (list-+ l1 l2)
  (if (empty? l1)
      '()
      (cons (+ (first l1) (first l2)) (list-+ (rest l1) (rest l2)))))

(define (list-scalar-* s l)
  (if (empty? l)
      '()
      (cons (* (first l) s) (list-scalar-* s (rest l)))))
