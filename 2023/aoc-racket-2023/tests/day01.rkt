#lang racket

(require rackunit)
(require rackunit/text-ui)

(require "../day01.rkt")

(define tests
  (test-suite
    "Day 1 tests"
    (let
      ([raw-input "1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet"]
       [part-two-raw-input "two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen"]
       [expected-part-one-answer 142]
       [expected-part-two-answer 281])
      (test-case
        "Test calibration-value-for-line"
        (check-equal? (calibration-value-for-line "1abc2") 12))
      (test-case
        "Test part one solution"
        (check-equal? (solution-part-one raw-input) expected-part-one-answer))
      (test-case
        "Test part two solution"
        (check-equal? (solution-part-two part-two-raw-input) expected-part-two-answer)))))

(run-tests tests)
