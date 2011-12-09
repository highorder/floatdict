===========
 FloatDict
===========

FloatDict is a sorted dictionary-like object where the keys are floats.

The implementation stores the keys and values in lists, which is
efficient for searching but not efficient for inserting or deleting.
Items are found using the bisection_ library

.. _bisection: http://docs.python.org/library/bisect.html

Start with an empty collection:
    >>> from floatdict import FloatDict
    >>> a = FloatDict()

Or initialize with an iterable:
    >>> a = FloatDict([(0.0, 1), (0.5, 2), (1.0, 3)])
    >>> a
    FloatDict([(0.0, 1), (0.5, 2), (1.0, 3)])

Get, set, and delete arbitary items:
    >>> a[-10] = 5
    >>> a[-10]
    5
    >>> del a[-10]
    >>> a[-10]
    Traceback (most recent call last):
        ...
    KeyError: -10

Values can be arbitrary Python objects:
    >>> a[0] = None

The collection is internally sorted and easily iterable.
    >>> a.keys()
    [0.0, 0.5, 1.0]
    >>> list(a)
    [(0.0, None), (0.5, 2), (1.0, 3)]

Quickly find key-value pairs near a specified key:
    >>> a = FloatDict([(0.0, 'zero'), (1.0, 'one'), (2.0, 'two')])
    >>> a.find_le(0.0)
    (0.0, 'zero')
    >>> a.find_lt(0.0)
    Traceback (most recent call last):
        ...
    ValueError
    >>> a.find_ge(0.0)
    (0.0, 'zero')
    >>> a.find_gt(0.0)
    (1.0, 'one')
