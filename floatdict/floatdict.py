"""
FloatDict is a sorted dictionary-like object where the keys are floats.

The implementation stores the keys and values in lists, which is
efficient for searching but not efficient for inserting or deleting.
@see http://docs.python.org/library/bisect.html
"""
from bisect import bisect_left, bisect_right

__all__ = ['FloatDict']

class FloatDict(object):
    """
    A sorted dictionary-like object where the keys are floats.

    Intialize with an empty collection or iterable.
    >>> a = FloatDict()
    >>> a
    FloatDict([])

    >>> a = FloatDict([(0.0, 1), (0.5, 2), (1.0, 3)])
    >>> a
    FloatDict([(0.0, 1), (0.5, 2), (1.0, 3)])
    """

    __slots__ = ('_keys', '_values')

    def __init__(self, iterable=()):
        self._keys = []
        self._values = []

        try:
            # Handle dictionaries.
            iterable = iterable.iteritems()
        except:
            pass

        # @todo: This is inefficient, should use quick-sort algorithm first.
        for k, v in iterable:
            self[k] = v

    def __len__(self):
        return len(self._keys)

    def _index(self, k):
        """Finds the index of an existing key k."""
        i = bisect_left(self._keys, k)
        if i != len(self._keys) and self._keys[i] == k:
            return i
        raise KeyError(k)

    def __getitem__(self, k):
        return self._values[self._index(k)]

    def __setitem__(self, k, v):
        k = float(k)
        try:
            # Replace an existing item:
            self._values[self._index(k)] = v
        except:
            # Insert a new item:
            i = bisect_left(self._keys, k)
            self._keys.insert(i, k)
            self._values.insert(i, v)

    def __delitem__(self, k):
        i = self._index(k)
        del self._keys[i]
        del self._values[i]

    def __contains__(self, k):
        try:
            i = self._index(k)
            return True
        except KeyError:
            return False

    def __iter__(self):
        for k,v in zip(self._keys, self._values):
            yield k,v

    def __reversed__(self):
        for k,v in zip(reversed(self._keys), reversed(self._values)):
            yield k,v

    def __reduce__(self):
        return self.__class__, (list(self),)

    def __str__(self):
        format_item = lambda item: "(%s, %s)" % item
        return "%s([%s])" % (self.__class__.__name__,
                             ", ".join(map(format_item, self)))
    __repr__ = __str__

    def keys(self):
        return list(self._keys)

    def find_lt(self, k):
        """key, value for rightmost entry with key < k"""
        i = bisect_left(self._keys, k)
        if i:
            return self._keys[i-1], self._values[i-1]
        raise ValueError

    def find_le(self, k):
        """key, value for rightmost entry with key <= k"""
        i = bisect_right(self._keys, k)
        if i:
            return self._keys[i-1], self._values[i-1]
        raise ValueError

    def find_gt(self, k):
        """key, value for leftmost entry with k > key"""
        i = bisect_right(self._keys, k)
        if i != len(self._keys):
            return self._keys[i], self._values[i]
        raise ValueError

    def find_ge(self, k):
        """key, value for leftmost entry with k >= key"""
        i = bisect_left(self._keys, k)
        if i != len(self._keys):
            return self._keys[i], self._values[i]
        raise ValueError
