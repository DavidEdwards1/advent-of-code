#lang racket

(require rackunit)
(require rackunit/text-ui)

(require "../day04.rkt")

(define tests
  (test-suite
    "Day 04"
    (test-case
      "is-winning-number? correctly identifies a winning number"
      (check-eq? (is-winning-number? (set 41 48 83 86 17) 48) #t))
    (test-case
      "all-winning-numbers returns all numbers that are winners"
      (check-equal?
        (all-winning-numbers (set 41 48 83 86 17) (set 83 86  6 31 17  9 48 53))
        (set 83 86 17 48)))
    (test-case
      "parse-card correctly parses a line of input"
      (check-equal?
        (parse-card "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
        (list (set 41 48 83 86 17) (set 83 86  6 31 17  9 48 53))))
    (test-case
      "solution-part-one gives the expected answer"
      (check-eq?
        (solution-part-one "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\nCard 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\nCard 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\nCard 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\nCard 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\nCard 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11")
        13))
    (test-case
      "solution-part-two gives the expected answer"
      (check-eq?
        (solution-part-two "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\nCard 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\nCard 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\nCard 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\nCard 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\nCard 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11")
        30))))

(run-tests tests)
