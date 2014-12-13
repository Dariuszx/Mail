__author__ = 'kacper'
import Login

assert(Login.valid_login('kacper', 'kacper') is False)
assert(Login.valid_login('linus', 'linus') is True)
assert(Login.valid_login('linus', 'linu') is False)
assert(Login.valid_login('linu', 'linus') is False)


print 'Test passed'