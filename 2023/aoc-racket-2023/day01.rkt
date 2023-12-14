#lang racket

(provide calibration-value-for-line solution-part-one solution-part-two)


(define calibration-value-for-line
  (compose1
    string->number
    list->string
    (lambda (l) (list (first l) (last l)))
    (curry filter char-numeric?)
    string->list))

(define (part-one-pre-processing input)
  (string-split input "\n"))

(define (part-two-pre-processing input)
  (string-split
    (left-to-right-replace
      input
      (hash
        "one" "1"
        "two" "2"
        "three" "3"
        "four" "4"
        "five" "5"
        "six" "6"
        "seven" "7"
        "eight" "8"
        "nine" "9"))
    "\n"))

(define solution-part-one
  (compose1
    (curry apply +)
    (curry map calibration-value-for-line)
    part-one-pre-processing))

(define solution-part-two
  (compose1
    (curry apply +)
    (curry map calibration-value-for-line)
    part-two-pre-processing))

(define (any-string-prefix input prefixes)
  (if (empty? prefixes)
      ""
      (if (string-prefix? input (first prefixes))
          (first prefixes)
          (any-string-prefix input (rest prefixes)))))

(define (left-to-right-replace input replacements)
  (if (eq? (string-length input) 0)
      ""
      (let*
        ([prefix (any-string-prefix input (hash-keys replacements))]
         [replaced (if (> (string-length prefix) 0)
                       prefix
                       (substring input 0 1))])
        (string-append
          (if (hash-has-key? replacements replaced)
              (hash-ref replacements replaced)
              replaced)
          (left-to-right-replace
            (substring input 1)
            replacements)))))

(define (ignore-parser input)
  (list '() (substring input 1)))

(define (one-parser input)
  (if (equal? "1" (substring input 0 1))
      (list '(1) (substring input 1))
      (list '() input)))

(define (only-one-parser input)
  (define (internal sub-input result)
    (one-parser sub-input))
  (internal input '()))

(define (parser-or p1 p2 input)
  (let
    ([result1 (p1 input)])
    (if (not (empty? (first result1)))
        result1
        (p2 input))))

(parser-or one-parser ignore-parser "two1nine")

(ignore-parser "two1nine")
(one-parser "1nine")
(only-one-parser "two1nine")

(define (part-one)
  (solution-part-one
    (port->string (open-input-file "./data/day01.txt") #:close? #t)))

(define (part-two)
  (solution-part-two
    (port->string (open-input-file "./data/day01.txt") #:close? #t)))
