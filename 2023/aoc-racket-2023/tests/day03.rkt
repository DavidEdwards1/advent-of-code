#lang racket

(require rackunit)
(require rackunit/text-ui)

(require "../day03.rkt")

(define tests
  (test-suite
    "Day 03"
    (test-case
      "Check if symbol next to number"
      (check-eq? (adjacent?
                  (number 467 '((0 0) (0 1) (0 2)))
                  (symbol "*" '(1 3))) #t))
    (test-case
      "Check part-numbers filters list of numbers to those adhjacent? to sym"
      (check-equal? (part-numbers
                      (list (number 467 '((0 0) (0 1) (0 2)))
                       (number 114 '((0 5) (0 6) (0 7)))
                       (number 35 '((2 2) (2 3)))
                       (number 633 '((2 6) (2 7))))
                      (list (symbol #\* '(1 3))
                       (symbol #\# '(3 6))))
                    (list (number 467 '((0 0) (0 1) (0 2)))
                       (number 35 '((2 2) (2 3)))
                       (number 633 '((2 6) (2 7))))))
    (test-case
      "Check that parse generates a list of numbers and a list of symbols"
      (check-equal? (parse "467..114..\n...*......")
                    (list
                      (list (number 467 '((0 0) (0 1) (0 2)))
                            (number 114 '((0 5) (0 6) (0 7))))
                      (list (symbol #\* '(1 3))))))))

(run-tests tests)
