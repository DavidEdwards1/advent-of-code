#lang racket

(require "utils.rkt")

(provide parse-card is-winning-number? all-winning-numbers solution-part-one solution-part-two)

(define (is-winning-number? winning-numbers num)
  (set-member? winning-numbers num))

(define (all-winning-numbers winning-numbers your-numbers)
  (set-intersect winning-numbers your-numbers))

(define (parse-card input)
  (map
    (compose
      (curry apply set)
      (curry map string->number)
      string-split)
    (string-split
      (second
        (string-split input ":"))
      "|")))

(define count-winning-numbers
  (compose
    length
    set->list
    (curry apply all-winning-numbers)))

(define score-n-winning-numbers
  (compose
    (curry expt 2)
    (lambda (x) (- x 1))))

(define solution-part-one
  (compose
    (curry apply +)
    (curry filter (curry <= 1))
    (curry map
      (compose
        score-n-winning-numbers
        count-winning-numbers
        parse-card))
    (lambda (x) (string-split x "\n"))))

(define (rolldown n start end i)
  (cond [(>= i end) '()]
        [(<  i start) (cons 0 (rolldown n start end (+ 1 i)))]
        [else (if (<= n 0)
                  (cons 0 (rolldown 0 start end (+ 1 i)))
                  (cons 1 (rolldown (- n 1) start end (+ 1 i))))]))

(define (calculate-total-cards winning-counts)
  ((compose
    (curry foldl
      (lambda (cards-to-add acc)
        (let* ([index (first cards-to-add)]
               [current-count (list-ref acc index)]
               [total-cards-to-add (list-scalar-* current-count (second cards-to-add))])
              (list-+ acc total-cards-to-add)))
      (ones (length winning-counts)))
    enumerate
    (curry map
      (lambda (x) (rolldown (second x) (+ 1 (first x)) (length winning-counts) 0)))
    enumerate)
   winning-counts))

(define solution-part-two
  (compose
    (curry apply +)
    calculate-total-cards
    (curry map
      (compose
        count-winning-numbers
        parse-card))
    (lambda (x) (string-split x "\n"))))

(define (part-one)
  (solution-part-one (file->string "./data/day04.txt")))

(define (part-two)
  (solution-part-two (file->string "./data/day04.txt")))
