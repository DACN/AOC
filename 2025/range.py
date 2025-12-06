import functools
import math

class RangeError(ValueError):
    pass

@functools.total_ordering
class Range:
    """A half-open integer range [d_from, d_to)"""
    
    def __init__(self, d_from, d_to=None, d_to_closed=None):
        # Empty range
        if d_from is None and d_to is None and d_to_closed is None:
            self.d_from = None
            self.d_to = None
            return

        # Check valid upper bound specification
        if d_to is not None and d_to_closed is not None:
            raise RangeError("Can only specify d_to or d_to_closed, not both")

        if d_from is None:
            raise RangeError("Lower bound cannot be None for a non-empty range")

        # Normalize upper bound
        if d_to_closed is not None:
            self.d_to = d_to_closed + 1
        elif d_to is not None:
            self.d_to = d_to
        else:
            raise RangeError("Upper bound must be specified")

        self.d_from = d_from

        # Check for empty or invalid range
        if self.d_from >= self.d_to:
            # canonical empty range
            self.d_from = None
            self.d_to = None

    @classmethod
    def empty(cls):
        return cls(None, None)

    def __repr__(self):
        if self.d_from is None:
            return "<Empty>"
        return f"[{self.d_from}, {self.d_to})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Range):
            return False
        return (self.d_from, self.d_to) == (other.d_from, other.d_to)

    def __lt__(self, other):
        # Empty ranges are always "largest"
        self_from = self.d_from if self.d_from is not None else math.inf
        other_from = other.d_from if other.d_from is not None else math.inf
        if self_from != other_from:
            return self_from < other_from
        self_to = self.d_to if self.d_to is not None else math.inf
        other_to = other.d_to if other.d_to is not None else math.inf
        return self_to < other_to

    def __contains__(self, x):
        if self.d_from is None:
            return False
        return self.d_from <= x < self.d_to

    def __mul__(self, other):
        """Intersection"""
        if self.d_from is None or other.d_from is None:
            return Range.empty()
        new_from = max(self.d_from, other.d_from)
        new_to = min(self.d_to, other.d_to)
        return Range(new_from, new_to)

    def overlaps(self, other):
        return (self * other).d_from is not None

    def adjoins(self, other):
        if self.d_from is None or other.d_from is None:
            return True
        return self.d_to == other.d_from or self.d_from == other.d_to

    def join(self, other):
        if not (self.overlaps(other) or self.adjoins(other)):
            raise RangeError("Ranges are disjoint")
        if self.d_from is None:
            return other
        if other.d_from is None:
            return self
        new_from = min(self.d_from, other.d_from)
        new_to = max(self.d_to, other.d_to)
        return Range(new_from, new_to)

    def __iter__(self):
        if self.d_from is None:
            return
        for i in range(self.d_from, self.d_to):
            yield i

    def __len__(self):
        if self.d_from is None:
            return 0
        return self.d_to - self.d_from


class ComplexRange:
    """Ordered set of non-overlapping Ranges"""

    def __init__(self, *ranges):
        self._ranges = []
        for r in ranges:
            self.add(r)

    def __repr__(self):
        if not self._ranges:
            return "<Empty>"
        return "(" + ", ".join(str(r) for r in self._ranges) + ")"

    def __len__(self):
        return sum(len(range) for range in self._ranges)

    def __iter__(self):
        for r in self._ranges:
            yield from r

    def __contains__(self, x):
        return any(x in r for r in self._ranges)

    def add(self, r):
        """Add and merge overlapping or adjoining ranges"""
        if r.d_from is None:
            return  # ignore empty range

        new_ranges = []
        merged = r
        for existing in self._ranges:
            if existing.overlaps(merged) or existing.adjoins(merged):
                merged = merged.join(existing)
            else:
                new_ranges.append(existing)
        new_ranges.append(merged)
        self._ranges = sorted(new_ranges)


# ✅ Example usage
if __name__ == "__main__":
    a = Range(4, 7)
    b = Range(8, 12)
    c = Range(10, 99)

    cr = ComplexRange()
    cr.add(a)
    cr.add(b)
    cr.add(c)

    print(cr)  # -> ([4, 7), [8, 99))
    print(list(cr))  # -> [4,5,6,8,9,...,98]
