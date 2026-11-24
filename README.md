# tiny_pairing_heap

A self-adjusting min-heap priority queue with amortized constant-time insertion, implemented in pure Python with no third-party dependencies.

```python
from tiny_pairing_heap import PairingHeap

h = PairingHeap()
h.push(3)
h.push(1)
h.push(2)

print(h.peek())   # 1
print(h.pop())    # 1
print(len(h))     # 2
```

You can order by a derived key without wrapping values:

```python
h = PairingHeap(key=lambda pair: pair[1])
h.push(("low", 10))
h.push(("high", 1))
print(h.pop())    # ("high", 1)
```

And meld two heaps in constant amortized time:

```python
a = PairingHeap()
b = PairingHeap()
a.push(4)
b.push(2)
a.meld(b)         # b is now empty
print(a.pop())    # 2
```

## Why this library exists

Binary heaps are simple and fast, but every insertion touches O(log n) nodes. A pairing heap is a self-adjusting structure: insertion and meld are O(1) amortized, and delete-min is O(log n) amortized. That makes it a good fit when you build many small heaps and merge them, or when insertion dominates deletion.

The trade-off is that the amortized bounds are not worst-case. A single delete-min can be slower than log n on an unlucky shape. This implementation follows the standard two-pass pairing strategy (pair siblings left-to-right, then merge the results right-to-left), which is what gives the structure its practical performance.

## The awkward edge

`meld` consumes the other heap and requires both heaps to use equivalent key functions. It does not check that the keys match, because comparing functions is not reliable in Python. If you meld heaps with different key functions, the ordering is whatever results from mixing those keys. Also, `meld` raises `ValueError` if you pass the same heap object, since that would create a cycle.

Iteration yields values in arbitrary order and does not consume the heap. `pop` and `peek` raise `IndexError` on an empty heap.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

