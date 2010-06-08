from __future__ import print_function

from itertools import imap, islice

def car(iter):
    assert isinstance(iter, Seq)
    return iter.car()

def cdr(iter):
    assert isinstance(iter, Seq)
    return iter.cdr()

class ConsCell(object):
    __slots__ = ["_realized", "_iterable", "val"]

    def __init__(self, iterable):
        self._realized = False
        self._iterable = iterable

    def _realize(self):
        self.val = (next(self._iterable), ConsCell(self._iterable))
        self._realized = True

    def get(self):
        if not self._realized:
            self._realize()
        return self.val

class ConsIterator(object):
    __slots__ = ["_head"]

    def __init__(self, head):
        self._head = head

    def __iter__(self):
        return self

    def next(self):
        this, next_ = self._head.get()
        self._head = next_
        return this

class Seq(object):
    __slots__ = ["_head"]

    def __init__(self, iterable):
        self._head = ConsCell(iter(iterable))

    def __iter__(self):
        return ConsIterator(self._head)

    def __nonzero__(self):
        try:
            self._head.get()
            return True
        except StopIteration:
            return False

    def __repr__(self):
        iterable = self.__iter__()
        lstr = ", ".join(imap(str, islice(iterable, 10)))
        try:
            next(iterable)
            return "Seq([%s, ...])" % lstr
        except StopIteration:
            return "Seq([%s])" % lstr

    def car(self):
        return self._head.get()[0]

    def cdr(self):
        try:
            s = self.__new__(type(self))
            s._head = self._head.get()[1]
            return s
        except StopIteration:
            pass

def thegen():
    for i in range(1, 5):
        print("gen", i)
        yield i

s = Seq(thegen())

def pr(s):
    print(repr(s))

pr(car(s))
pr(car(s))
pr(cdr(s))
pr(list(cdr(s)))

def test_huge_sum():
    s = Seq(xrange(1000000))
    the_sum = 0
    while s:
        the_sum += car(s)
        s = cdr(s)
    print("the sum", the_sum)
