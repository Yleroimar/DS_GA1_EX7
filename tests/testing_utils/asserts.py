import gc
import unittest
from typing import Callable, Set, Tuple

from utils.distributed.node_ref import NodeRef
from utils.ring import Ring


KeySetConstructor = Callable[[int, int], Tuple[Set[int], Set[int]]]


def init_key_set_constructor(ks_min: int, ks_max: int) -> KeySetConstructor:
    def get_complement(keys: {int}) -> {int}:
        return set(key for key in range(ks_min, ks_max + 1) if key not in keys)


    def add_complement(keys: {int}) -> ({int}, {int}):
        return keys, get_complement(keys)


    def key_set_constructor(first: int, last: int) -> ({int}, {int}):
        if first <= last:
            return add_complement(set(range(first, last + 1)))

        return add_complement(set(list(range(first, ks_max + 1)) + list(range(ks_min, last + 1))))


    return key_set_constructor


def init_ring(ks_start: int, ks_end: int, node_values: [int], shortcuts: [(int, int)]) -> Ring:
    return Ring((ks_start, ks_end), node_values, shortcuts)


class AddedAsserts(unittest.TestCase):
    """ NB! Make sure your Ring has a destructor, or find another way to free up resources. """


    def tearDown(self) -> None:
        gc.collect()  # need to free up resources otherwise tests are gonna conflict with each other


    def assertExit(self, action: callable):
        self.assertRaises(SystemExit, action)


    def assertRing(self, ring: Ring, *expected_listed: str, sanity_only: bool = False):
        actual_lines = ring.testing_list_as_str().split("\n")
        n_lines = len(actual_lines)

        for i, expected in enumerate(expected_listed):
            self.assertEqual(expected,
                             actual_lines[i] if i < n_lines else None,
                             msg=f"Listing line {i + 1}")

        if sanity_only:
            return

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
        self.skipTest("Not implemented.")


    def assertRingLeave(self, ring: Ring, leaving: int, *expected_listed: str):
        ring.leave(leaving)
        self.assertRing(ring, *expected_listed)


    def assertRingShortcut(self, ring: Ring, source: int, target: int, *expected_listed: str):
        ring.add_shortcut(source, target)
        self.assertRing(ring, *expected_listed)


    def assertRingLookup(self, ring: Ring, key: int, starting_value: int = None,
                         expected_node: int = None, expected_requests: int = None):
        node, n_requests = ring.lookup(key, starting_value)

        self.assertEqual(expected_node, None if node is None else node.get_value(),
                         msg=f"Container node when looking up key {key}"
                             f" starting from node with value {starting_value}")

        if expected_requests is None:
            return

        self.assertEqual(expected_requests, n_requests,
                         msg=f"Number of requests performed when looking up key {key}"
                             f" starting from node with value {starting_value}")


    def assertNodeKeys(self, ring: Ring, node_value: int,
                       expected_keys: {int}, unexpected_keys: {int}):
        node: NodeRef = NodeRef(node_value)

        for key in expected_keys:
            self.assertTrue(key in node,
                            msg=f"Node with value {node_value} should contain the key {key}")

        for key in unexpected_keys:
            self.assertFalse(key in node,
                             msg=f"Node with value {node_value} should not contain the key {key}")


    def assertRingKeys(self, ring: Ring, values_with_expected_and_unexpected_keys: (int, {int})):
        for value, expected_keys_and_unexpected_keys in values_with_expected_and_unexpected_keys:
            expected_keys, unexpected_keys = expected_keys_and_unexpected_keys
            self.assertNodeKeys(ring, value, expected_keys, unexpected_keys)
