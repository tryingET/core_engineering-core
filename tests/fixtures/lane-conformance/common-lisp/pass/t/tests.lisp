(defpackage :my-system/tests
  (:use :cl :my-system)
  (:export #:run-tests))
(in-package :my-system/tests)

(defun run-tests ()
  (let ((ok (= 3 (add 1 2))))
    (format t "~&add: ~:[FAIL~;PASS~]~%" ok)
    ok))
