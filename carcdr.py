from itertools import imap, islice

def car(iter):
    assert isinstance(iter, Seq)
    return iter.car()

def cdr(iter):
    assert isinstance(iter, Seq)
    return iter.cdr()

def cons(p1, p2):
    assert isinstance(p2, Seq)
    seq = Seq.__new__(Seq)
    seq._head = ConsCell(p1, p2)
    return seq

class SeqConsCell(object):
    __slots__ = ["_realized", "_iterable", "val"]

    def __init__(self, iterable):
        self._realized = False
        self._iterable = iterable

    def _realize(self):
        self.val = (next(self._iterable), SeqConsCell(self._iterable))
        self._realized = True

    def get(self):
        if not self._realized:
            self._realize()
        return self.val

class ConsCell(object):
    __slots__ = ["_car", "_cdr"]

    def __init__(self, car, cdr):
        self._car = car
        self._cdr = cdr

    def get(self):
        return self._car, self._cdr._head

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
        self._head = SeqConsCell(iter(iterable))

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
        try:
            return self._head.get()[0]
        except StopIteration:
            pass

    def cdr(self):
        try:
            s = self.__new__(type(self))
            s._head = self._head.get()[1]
            return s
        except StopIteration:
            return self
