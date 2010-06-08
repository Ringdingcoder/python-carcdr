from __future__ import print_function

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

    def __repr__(self):
        # XXX use islice
        return "Seq(%r)" % list(self.__iter__())

    def car(self):
        return self._head.get()[0]

    def cdr(self):
        s = self.__new__(type(self))
        s._head = self._head.get()[1]
        return s

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
