#lang racket

(require rackunit)
(require rackunit/text-ui)

(require "../day02.rkt")

(define tests
  (test-suite
    "Day 2 tests"
    (let
      ([raw-input "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\nGame 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\nGame 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\nGame 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\nGame 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]
       [expected-first-game (list
                              (list 'id 1)
                              (list 'reveals (list
                                                #hash((blue . 3)
                                                      (red . 4))
                                                #hash((red . 1)
                                                      (green . 2)
                                                      (blue . 6))
                                                #hash((green . 2)))))]
       [expected-part-one-answer 8])
      (test-case
        "first game parses correctly"
        (check-equal?
          (parse-game "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
          expected-first-game))
      (test-case
        "first game required balls"
        (check-equal? (game-minimum-balls expected-first-game) #hash((blue . 6) (red . 4) (green . 2))))
      (test-case
        "game-possible? gives expected answers"
        (check-equal? (game-possible? #hash((red . 12) (green . 13) (blue . 14)) expected-first-game) (list '(id 1) #t)))
      (test-case
        "part-one-solution gives expected answer"
        (check-eq? (solution-part-one raw-input) expected-part-one-answer))
      (test-case
        "part-two-solution gives expected answer"
        (check-eq? (solution-part-two raw-input) 2286)))))

(run-tests tests)
