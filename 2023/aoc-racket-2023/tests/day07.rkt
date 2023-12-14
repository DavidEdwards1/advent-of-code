#lang racket

(require rackunit)
(require rackunit/text-ui)

(require "../day07.rkt")

(define tests
  (test-suite
    "Day 07"
    (test-case
      "solution-part-one gives the expected result on the test case"
      (check-eq? (solution-part-one "32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483") 6440))
    (test-case
      "solution-part-two gives the expected result on the test case"
      (check-eq? (solution-part-two "32T3K 765\nT55J5 684\nKK677 28\nKTJJT 220\nQQQJA 483") 5905))
    (test-case
      "hand< gives the correct ordering"
      (check-eq?
        (hand< (hand "KTJJT" "two" 220) (hand "T55J5" "three" 684))
        #t))
    (test-case
      "sort-hands sorts into the correct order"
      (check-equal? (sort-hands
                      (list
                        (hand "QQQJA" "three" 483)
                        (hand "T55J5" "three" 684)
                        (hand "KK677" "two" 28)
                        (hand "KTJJT" "two" 220)
                        (hand "32T3K" "one" 765)))
                    (list
                        (hand "32T3K" "one" 765)
                        (hand "KTJJT" "two" 220)
                        (hand "KK677" "two" 28)
                        (hand "T55J5" "three" 684)
                        (hand "QQQJA" "three" 483))))
      (test-case
        "parse-hand gives the expected hand"
        (check-equal? (parse-hand "KK677 28") (hand "KK677" "two" 28)))
      (test-case
      "part-two-hand< gives the correct ordering"
      (check-eq? (part-two-hand< (hand "JKKK2" "four" 220) (hand "99992" "four" 684)) #t)
      (check-eq? (part-two-hand< (hand "JQQQ3" "four" 220) (hand "JQQQT" "four" 684)) #t))
      (test-case
        "check hand-type-from-cards-part-two gives expected answer"
        (check-eq? (hand-type-from-cards-part-two "QQQQQ") "five")
        (check-eq? (hand-type-from-cards-part-two "QQQQJ") "five")
        (check-eq? (hand-type-from-cards-part-two "QQQJJ") "five")
        (check-eq? (hand-type-from-cards-part-two "QQJJJ") "five")
        (check-eq? (hand-type-from-cards-part-two "QJJJJ") "five")
        (check-eq? (hand-type-from-cards-part-two "JJJJJ") "five")
        (check-eq? (hand-type-from-cards-part-two "QQQQT") "four")
        (check-eq? (hand-type-from-cards-part-two "QQQJT") "four")
        (check-eq? (hand-type-from-cards-part-two "QQJJT") "four")
        (check-eq? (hand-type-from-cards-part-two "QJJJT") "four")
        (check-eq? (hand-type-from-cards-part-two "QQQTT") "full")
        (check-eq? (hand-type-from-cards-part-two "QQJTT") "full")
        (check-eq? (hand-type-from-cards-part-two "QQQT9") "three")
        (check-eq? (hand-type-from-cards-part-two "QQJT9") "three")
        (check-eq? (hand-type-from-cards-part-two "QJJT9") "three")
        (check-eq? (hand-type-from-cards-part-two "QQTT9") "two")
        (check-eq? (hand-type-from-cards-part-two "QQT98") "one")
        (check-eq? (hand-type-from-cards-part-two "QJT98") "one")
        (check-eq? (hand-type-from-cards-part-two "QT987") "high")
        (check-eq? (hand-type-from-cards-part-two "22AAA") "full"))
      (test-case
        "parse-hand-part-two gives the expected hand"
        (check-equal? (parse-hand-part-two "KK677 28") (hand "KK677" "two" 28))
        (check-equal? (parse-hand-part-two "KTJJT 220") (hand "KTJJT" "four" 220))
        (check-equal? (parse-hand-part-two "TTJ55 28") (hand "TTJ55" "full" 28)))))

(run-tests tests)

; "
; 32T3K 765
; T55J5 684
; KK677 28
; KTJJT 220
; QQQJA 483"
