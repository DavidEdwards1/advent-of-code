#lang racket

(require rackunit)
(require rackunit/text-ui)

(define (part-one-solution)
  (apply +
    (map
      (curry apply manhatten-distance)
      (point-pairs (list (point 0 4) (point 1 9) (point 2 0)
                         (point 5 8) (point 6 1) (point 7 12)
                         (point 10 9) (point 11 0) (point 11 5))))))

(struct point (r c) #:transparent)

(define (empty-rows rmax points)
  (let ([occupied-rows (map point-r points)])
       (sort (set-subtract (range rmax) occupied-rows) <)))

(define (empty-cols cmax points)
  (let ([occupied-cols (map point-c points)])
       (sort (set-subtract (range cmax) occupied-cols) <)))

(define (add-row pivot points)
  (map (lambda (p) (let ([r (point-r p)] [c (point-c p)]) (point (if (> r pivot) (add1 r) r) c))) points))

(define (add-col points pivot)
  (map (lambda (p) (let ([r (point-r p)] [c (point-c p)]) (point r (if (> c pivot) (add1 c) c)))) points))

(define (expand start rows cols)
  (foldl add-row start rows))

(define (point-pairs points)
  (combinations points 2))

(define (manhatten-distance p1 p2)
  (+ (abs (- (point-r p1) (point-r p2)))
     (abs (- (point-c p1) (point-c p2)))))

; TESTS
(define tests
  (test-suite
    "Day 11"
    (let
      ([example-points (list (point 0 3) (point 1 7) (point 2 0)
                             (point 4 6) (point 5 1) (point 6 9)
                             (point 8 7) (point 9 0) (point 9 4))]
       [example-expanded-points (list (point 0 4) (point 1 9) (point 2 0)
                                      (point 5 8) (point 6 1) (point 7 12)
                                      (point 10 9) (point 11 0) (point 11 5))])
      (test-case
        "part-one-solution gives the expected answer for test case"
        (check-eq? (part-one-solution) 374))
      (test-case
        "manhatten-distance gives expected answer"
        ; galaxies 5 and 9
        (check-eq? (manhatten-distance (point 6 1) (point 11 5)) 9)
        ; galaxies 1 and 7
        (check-eq? (manhatten-distance (point 0 4) (point 10 9)) 15)
        ; galaxies 3 and 6
        (check-eq? (manhatten-distance (point 2 0) (point 7 12)) 17)
        ; galaxies 8 and 9
        (check-eq? (manhatten-distance (point 11 0) (point 11 5)) 5))
      (test-case
        "point-pairs gives correct number of combinations of points"
        (check-eq?
          (length (point-pairs example-expanded-points))
          36))
      (test-case
        "empty-rows gives the correct set of empty rows for the example"
        (check-equal? (empty-rows 10 example-points) '(3 7)))
      (test-case
        "empty-cols gives the correct set of empty cols for the example"
        (check-equal? (empty-cols 10 example-points) '(2 5 8)))
      (test-case
        "add-row adds a row to all point after pivot"
        (check-equal? (add-row 2 (list (point 0 1) (point 3 4))) (list (point 0 1) (point 4 4))))
      (test-case
        "add-col adds a col to all points after pivot"
        (check-equal? (add-col (list (point 0 2) (point 3 4)) 1) (list (point 0 3) (point 3 5))))
      (test-case
        "expand transforms example into expanded example"
        (check-equal? (expand example-points '(3 7) '()) example-expanded-points)))))

(run-tests tests)
