#lang racket

(require "utils.rkt")

(define (ways-to-beat-record t record)
  ((compose
    length
    (curry filter (curry < record))
    (curry map (curry apply *)))
    (zip (range (+ 1 t)) (reverse (range (+ 1 t))))))

(define (parse-input input)
  (apply zip
    (map
    (compose
      (curry map string->number)
      rest
      string-split)
    (string-split input "\n"))))

(define (parse-input-part-two input)
  (map
    (compose
      string->number
      string-append*
      rest
      string-split)
    (string-split input "\n")))

(define (solution-part-one input)
  (apply *
    (map
      (curry apply ways-to-beat-record)
      (parse-input input))))

(define (solution-part-two input)
  (apply ways-to-beat-record
    (parse-input-part-two input)))

(solution-part-two "Time:      7  15   30\nDistance:  9  40  200")

(define (part-one)
  (solution-part-one (file->string "./data/day06.txt")))

(define (part-two)
  (solution-part-two (file->string "./data/day06.txt")))

(define (area p diff)
  (* (/ (- p diff) 2) (/ (+ p diff) 2)))
