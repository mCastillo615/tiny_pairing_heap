"""Pairing heap implementation.

A pairing heap is a self-adjusting heap with excellent amortized bounds:
insert is O(1) amortized, meld is O(1), and delete-min is O(log n) amortized.
It is simpler to implement than Fibonacci heaps while having similarly good
practical performance for many workloads.

This implementation stores a single tree whose root is the minimum element.
Each node keeps a list of children. The pairing operation is used during
delete-min: the children of the removed root are paired up left-to-right and
merged, then the resulting roots are merged right-to-left.
"""

from __future__ import annotations

from typing import Any, Callable, Iterator, Optional


class _Node:
    """Internal node of a pairing heap.

    We use a class with __slots__ to keep per-node overhead low; a heap may
    hold many nodes and each node has only a value, an optional left-child
    sibling link, and a next-sibling link.  The sibling links form a linked
    list of children for each parent.
    """

    __slots__ = ("value", "child", "sibling")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.child: Optional[_Node] = None
        self.sibling: Optional[_Node] = None


class PairingHeap:
    """A min-heap priority queue using a pairing heap.

    The heap is ordered by a key function.  By default the identity function
    is used, so values must be comparable with ``<``.  Pass ``key`` to order
    by a derived value without wrapping every element.

    ``PairingHeap`` is not thread-safe.  It is iterable in arbitrary order;
    iteration does not consume the heap.

    Example:
        >>> h = PairingHeap()
        >>> h.push(3)
        >>> h.push(1)
        >>> h.push(2)
        >>> h.pop()
        1
        >>> h.peek()
        2
        >>> len(h)
        2
    """

    __slots__ = ("_root", "_size", "_key")

    def __init__(self, key: Optional[Callable[[Any], Any]] = None) -> None:
        self._root: Optional[_Node] = None
        self._size = 0
        self._key = key if key is not None else (lambda x: x)

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def __iter__(self) -> Iterator[Any]:
        """Yield all values in arbitrary order.

        The traversal is iterative to avoid recursion limits on deep heaps.
        """
        if self._root is None:
            return
        stack = [self._root]
        while stack:
            node = stack.pop()
            yield node.value
            child = node.child
            while child is not None:
                stack.append(child)
                child = child.sibling

    def push(self, value: Any) -> None:
        """Insert *value* into the heap.  O(1) amortized."""
        node = _Node(value)
        if self._root is None:
            self._root = node
        else:
            self._root = self._merge(self._root, node)
        self._size += 1

    def peek(self) -> Any:
        """Return the smallest value without removing it.

        Raises IndexError if the heap is empty.
        """
        if self._root is None:
            raise IndexError("peek from empty PairingHeap")
        return self._root.value

    def pop(self) -> Any:
        """Remove and return the smallest value.

        Raises IndexError if the heap is empty.
        """
        if self._root is None:
            raise IndexError("pop from empty PairingHeap")
        value = self._root.value
        self._root = self._merge_pairs(self._root.child)
        self._size -= 1
        return value

    def meld(self, other: "PairingHeap") -> None:
        """Merge *other* into this heap, consuming it.

        Both heaps must use equivalent key functions.  After the call, *other*
        is empty.  This is O(1) amortized.
        """
        if other is self:
            raise ValueError("cannot meld a PairingHeap with itself")
        if other._root is None:
            return
        if self._root is None:
            self._root = other._root
        else:
            self._root = self._merge(self._root, other._root)
        self._size += other._size
        other._root = None
        other._size = 0

    def _merge(self, a: _Node, b: _Node) -> _Node:
        """Merge two roots, returning the new root.

        The root with the smaller key becomes the parent.  Ties keep *a* as
        the root, which makes the result deterministic for equal keys.
        """
        if self._key(b.value) < self._key(a.value):
            a, b = b, a
        b.sibling = a.child
        a.child = b
        return a

    def _merge_pairs(self, first: Optional[_Node]) -> Optional[_Node]:
        """Merge a linked list of sibling roots using the two-pass pairing method.

        The first pass merges adjacent pairs left-to-right.  The second pass
        merges the resulting roots right-to-left.  This gives the amortized
        bounds that make pairing heaps interesting.
        """
        if first is None:
            return None
        # First pass: pair up siblings.
        pairs = []
        node = first
        while node is not None:
            a = node
            b = a.sibling
            if b is None:
                pairs.append(a)
                break
            nxt = b.sibling
            a.sibling = None
            b.sibling = None
            pairs.append(self._merge(a, b))
            node = nxt
        # Second pass: merge from right to left.
        result = pairs.pop()
        while pairs:
            result = self._merge(pairs.pop(), result)
        return result
