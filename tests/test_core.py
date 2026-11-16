import unittest

from tiny_pairing_heap import PairingHeap


class TestPairingHeap(unittest.TestCase):
    def test_empty(self):
        h = PairingHeap()
        self.assertEqual(len(h), 0)
        self.assertFalse(h)
        with self.assertRaises(IndexError):
            h.peek()
        with self.assertRaises(IndexError):
            h.pop()
        self.assertEqual(list(h), [])

    def test_push_and_pop_sorted(self):
        h = PairingHeap()
        values = [5, 1, 9, 3, 7, 2, 8, 4, 6, 0]
        for v in values:
            h.push(v)
        self.assertEqual(len(h), len(values))
        self.assertTrue(h)
        out = [h.pop() for _ in range(len(values))]
        self.assertEqual(out, sorted(values))
        self.assertEqual(len(h), 0)

    def test_peek_does_not_remove(self):
        h = PairingHeap()
        h.push(42)
        h.push(7)
        self.assertEqual(h.peek(), 7)
        self.assertEqual(len(h), 2)
        self.assertEqual(h.pop(), 7)
        self.assertEqual(h.peek(), 42)

    def test_duplicates(self):
        h = PairingHeap()
        for v in [2, 2, 1, 1, 3, 3]:
            h.push(v)
        out = [h.pop() for _ in range(6)]
        self.assertEqual(out, [1, 1, 2, 2, 3, 3])

    def test_key_function(self):
        # Order by the second element of a tuple.
        h = PairingHeap(key=lambda pair: pair[1])
        h.push(("a", 3))
        h.push(("b", 1))
        h.push(("c", 2))
        self.assertEqual(h.pop(), ("b", 1))
        self.assertEqual(h.pop(), ("c", 2))
        self.assertEqual(h.pop(), ("a", 3))

    def test_meld(self):
        a = PairingHeap()
        b = PairingHeap()
        for v in [4, 1, 7]:
            a.push(v)
        for v in [3, 9, 2]:
            b.push(v)
        a.meld(b)
        self.assertEqual(len(a), 6)
        self.assertEqual(len(b), 0)
        out = [a.pop() for _ in range(6)]
        self.assertEqual(out, [1, 2, 3, 4, 7, 9])

    def test_meld_empty(self):
        a = PairingHeap()
        b = PairingHeap()
        b.push(10)
        a.meld(b)
        self.assertEqual(len(a), 1)
        self.assertEqual(a.pop(), 10)
        self.assertEqual(len(b), 0)
        c = PairingHeap()
        d = PairingHeap()
        d.push(5)
        d.meld(c)
        self.assertEqual(d.pop(), 5)

    def test_meld_into_empty(self):
        a = PairingHeap()
        b = PairingHeap()
        a.push(1)
        b.push(2)
        b.meld(a)
        self.assertEqual(len(b), 2)
        self.assertEqual(b.pop(), 1)
        self.assertEqual(b.pop(), 2)
        self.assertEqual(len(a), 0)

    def test_meld_self_raises(self):
        h = PairingHeap()
        h.push(1)
        with self.assertRaises(ValueError):
            h.meld(h)
        self.assertEqual(len(h), 1)

    def test_iteration_arbitrary_order(self):
        h = PairingHeap()
        values = [3, 1, 4, 1, 5, 9, 2, 6]
        for v in values:
            h.push(v)
        self.assertEqual(sorted(h), sorted(values))
        # Iteration must not consume the heap.
        self.assertEqual(len(h), len(values))
        self.assertEqual(h.peek(), 1)

    def test_large_heap(self):
        # Exercise the two-pass pairing on a deep tree.
        h = PairingHeap()
        n = 1000
        for i in range(n):
            h.push((i * 7919) % n)
        out = [h.pop() for _ in range(n)]
        self.assertEqual(out, list(range(n)))

    def test_string_values(self):
        h = PairingHeap()
        for s in ["banana", "apple", "cherry", "date"]:
            h.push(s)
        self.assertEqual(h.pop(), "apple")
        self.assertEqual(h.pop(), "banana")
        self.assertEqual(h.pop(), "cherry")
        self.assertEqual(h.pop(), "date")

    def test_mixed_pop_push(self):
        h = PairingHeap()
        h.push(5)
        h.push(2)
        self.assertEqual(h.pop(), 2)
        h.push(1)
        h.push(8)
        self.assertEqual(h.pop(), 1)
        self.assertEqual(h.pop(), 5)
        h.push(3)
        self.assertEqual(h.pop(), 3)
        self.assertEqual(h.pop(), 8)
        self.assertEqual(len(h), 0)


if __name__ == "__main__":
    unittest.main()
