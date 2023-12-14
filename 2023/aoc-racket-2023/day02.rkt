#lang racket

(require racket/hash)

(provide parse-game game-minimum-balls game-possible? solution-part-one solution-part-two)

(define (solution-part-one input)
  (apply +
    (map
      (compose second first)
      (filter
        (lambda (x) (second x))
        (map
          (compose
            (curry game-possible? #hash((red . 12) (green . 13) (blue . 14)))
            parse-game)
          (string-split input "\n"))))))

(define (solution-part-two input)
  (apply +
    (map
      (compose
        (curry apply *)
        hash-values
        game-minimum-balls
        parse-game)
      (string-split input "\n"))))

(define (parse-game game)
  (match-let
    ([(list id reveals) (string-split game ":")])
    (list
      (list 'id (string->number (last (string-split id " "))))
      (list
        'reveals
        (map parse-reveal (string-split reveals ";"))))))

(define (parse-reveal reveal)
  (make-immutable-hash
    (map
      (lambda (y) (cons (string->symbol (last y)) (string->number (first y))))
      (map
        (lambda (x) (string-split x " "))
        (string-split (string-trim reveal) ", ")))))

(define (game-minimum-balls game)
  (apply hash-union
    (second (second game))
    #:combine/key (lambda (_ v1 v2) (max v1 v2))))

(define (all l)
  (foldl
    (lambda (x y) (and x y))
    #t
    l))

(define (game-possible? given-ball-set game)
  (let ([required-balls (game-minimum-balls game)])
    (list (first game)
      (all
        (hash-map
          required-balls
          (lambda (k v) (and (hash-has-key? given-ball-set k)
                            (>= (hash-ref given-ball-set k) v))))))))

(define (part-one)
  (solution-part-one
    (port->string (open-input-file "./data/day02.txt") #:close? #t)))

(define (part-two)
  (solution-part-two
    (port->string (open-input-file "./data/day02.txt") #:close? #t)))
