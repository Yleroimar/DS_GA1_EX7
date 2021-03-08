import unittest

from utils.ring import Ring


class AddedAsserts(unittest.TestCase):
    def assertRing(self, ring: Ring, *expected_listed: str):
        actual_lines = ring.list_as_str().split("\n")
        n_lines = len(actual_lines)

        for i, expected in enumerate(expected_listed):
            self.assertEqual(expected,
                             actual_lines[i] if i < n_lines else None,
                             msg=f"Listing line {i + 1}")

    def assertRingJoin(self, ring: Ring, joining: int, *expected_listed: str):
        ring.join(joining)
        self.assertRing(ring, *expected_listed)

    def assertRingRemove(self, ring: Ring, removing: [int], *expected_listed: str):
        ring.leave(removing)
        self.assertRing(ring, *expected_listed)

    def assertRingLeave(self, ring: Ring, leaving: int, *expected_listed: str):
        self.assertRingRemove(ring, [leaving], *expected_listed)

    def assertRingShortcut(self, ring: Ring, source: int, target: int, *expected_listed: str):
        ring.add_shortcut(source, target)
        self.assertRing(ring, *expected_listed)

    def assertRingLookup(self, ring: Ring, key: int, starting_value: int = None,
                         expected_node: int = None, expected_requests: int = None):
        assert (expected_requests is None) == (expected_node is None)

        result = ring.lookup(key, starting_value)

        self.assertEqual((result, result) if result is None else result,
                         (expected_node, expected_requests),
                         msg="Lookup results (node, requests)")
