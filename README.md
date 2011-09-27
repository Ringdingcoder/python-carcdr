car, cdr & cons for Python
==========================

Some preliminaries:

```python
>>> from carcdr import car, cdr, cons, Seq
>>> def thegen(m):
...     for i in range(1, m):
...         print "gen", i
...         yield i
... 
```

Once we’ve made a Seq out of the iterator, it behaves just as we would expect. Note that the iterator is consumed lazily:

```python
>>> s = Seq(thegen(5))
>>> car(s)
gen 1
1
>>> car(s)
1
>>> cdr(s)
gen 2
gen 3
gen 4
Seq([2, 3, 4])
```

We can also make a list from it again:

```python
>>> list(cdr(s))
[2, 3, 4]
```

Doesn’t require an over-night run (but it’s not particularly fast either):

```python
>>> def test_huge_sum(s):
...     s = Seq(xrange(1000000))
...     the_sum = 0
...     while s:
...         the_sum += car(s)
...         s = cdr(s)
...     print "the sum", the_sum
...
>>> test_huge_sum(Seq(xrange(1000000)))
the sum 499999500000
```

Let’s play around a bit with cons:

```python
>>> sc = cdr(s)
>>> cons(0, cons(1, sc))
Seq([0, 1, 2, 3, 4])
>>> sc
Seq([2, 3, 4])
>>> cons(0, cons(1, sc))
Seq([0, 1, 2, 3, 4])
```

And finally, just to let you know you’re safe. Note again that the iterator is just consumed as far as necessary:

```python
>>> Seq(xrange(1000000))
Seq([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...])
>>> Seq(thegen(1000000))
gen 1
gen 2
gen 3
gen 4
gen 5
gen 6
gen 7
gen 8
gen 9
gen 10
gen 11
Seq([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...])
```
