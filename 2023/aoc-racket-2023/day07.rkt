#lang racket

(require "./utils.rkt")

(provide hand hand< sort-hands parse-hand solution-part-one solution-part-two parse-hand-part-two hand-type-from-cards-part-two part-two-hand<)

; type is one of:
;   Five of a kind - five
;   Four of a kind - four
;   Full house - full
;   Three of a kind - three
;   Two pair - two
;   One pair - one
;   High card - high
(struct hand (cards type bid) #:transparent)

(define (frequencies lst)
  (foldl
    (lambda (x ht) (hash-update ht x add1 0))
    #hash()
    lst))

(define list->ordering-hash
  (compose
    make-hash
    (curry map (compose (curry apply cons) reverse))
    enumerate))

(define (hand-type-from-cards cards)
  (let* ([frequency-table (sort (hash-values (frequencies (string->list cards))) >)]
         [max-same (first frequency-table)])
       (cond [(= max-same 5) "five"]
             [(= max-same 4) "four"]
             [(= max-same 3) (if (= 2 (second frequency-table)) "full" "three")]
             [(= max-same 2) (if (= 2 (second frequency-table)) "two" "one")]
             [(= max-same 1) "high"])))

(define (parse-hand input)
  (match-let ([(list cards bid) (string-split input)])
    (hand cards (hand-type-from-cards cards) (string->number bid))))

(define (cards< c1 c2)
  (let ([card-ordering (list->ordering-hash (string->list "23456789TJQKA"))])
  (if (empty? c1)
      (if (empty? c2)
        #f
        #t)
      (if (empty? c2)
          #t
          (if (eq? (first c1) (first c2))
              (cards< (rest c1) (rest c2))
              (< (hash-ref card-ordering (first c1)) (hash-ref card-ordering (first c2))))))))

(define (hand< h1 h2)
  (let
    ([type-ordering (list->ordering-hash '("high" "one" "two" "three" "full" "four" "five"))]
     [h1-type (hand-type h1)]
     [h2-type (hand-type h2)])
     (if (eq? h1-type h2-type)
      (cards< (string->list (hand-cards h1)) (string->list (hand-cards h2)))
      (< (hash-ref type-ordering h1-type) (hash-ref type-ordering h2-type)))))

(define (sort-hands lhands)
  (sort lhands hand<))

(define (solution-part-one input)
  (let ([sorted (sort-hands (map parse-hand (string-split input "\n")))])
       (apply +
          (map
            (curry apply *)
            (map
              (lambda (x) (list (add1 (first x)) (hand-bid (second x))))
              (enumerate sorted))))))


(define (hand-type-from-cards-part-two cards)
  (let* ([card-frequencies (frequencies (string->list cards))]
         [jokers (hash-ref card-frequencies #\J 0)]
         [frequency-table (sort (hash-values (hash-remove card-frequencies #\J)) >)]
         [max-same (+ (if (empty? frequency-table) 0 (first frequency-table)) jokers)])
       (cond [(= max-same 5) "five"]
             [(= max-same 4) "four"]
             [(= max-same 3) (if (= 2 (second frequency-table)) "full" "three")]
             [(= max-same 2) (if (= 2 (second frequency-table)) "two" "one")]
             [(= max-same 1) "high"])))

(define (parse-hand-part-two input)
  (match-let ([(list cards bid) (string-split input)])
    (hand cards (hand-type-from-cards-part-two cards) (string->number bid))))

(define (part-two-cards< c1 c2)
  (let ([card-ordering (list->ordering-hash (string->list "J23456789TQKA"))])
  (if (empty? c1)
      (if (empty? c2)
        #f
        #t)
      (if (empty? c2)
          #t
          (if (eq? (first c1) (first c2))
              (part-two-cards< (rest c1) (rest c2))
              (< (hash-ref card-ordering (first c1)) (hash-ref card-ordering (first c2))))))))

(define (part-two-hand< h1 h2)
  (let
    ([type-ordering (list->ordering-hash '("high" "one" "two" "three" "full" "four" "five"))]
     [h1-type (hand-type h1)]
     [h2-type (hand-type h2)])
     (if (eq? h1-type h2-type)
      (part-two-cards< (string->list (hand-cards h1)) (string->list (hand-cards h2)))
      (< (hash-ref type-ordering h1-type) (hash-ref type-ordering h2-type)))))

(define (sort-hands-part-two lhands)
  (sort lhands part-two-hand<))

(define (solution-part-two input)
  (let ([sorted (sort-hands-part-two (map parse-hand-part-two (string-split input "\n")))])
       (apply +
          (map
            (curry apply *)
            (map
              (lambda (x) (list (add1 (first x)) (hand-bid (second x))))
              (enumerate sorted))))))

(define (part-one)
  (solution-part-one (port->string (open-input-file "./data/day07.txt") #:close? #t)))

(define (part-two)
  (solution-part-two (port->string (open-input-file "./data/day07.txt") #:close? #t)))
