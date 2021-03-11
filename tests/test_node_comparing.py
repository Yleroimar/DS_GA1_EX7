import random

from tests.testing_utils.asserts import AddedAsserts

from utils.node_old import Node


class TestNodeComparing(AddedAsserts):

    def testComparing01(self):
        self.assertEqual(Node(5, 1, 10), Node(5, 1, 10))

    def testComparing02(self):
        self.assertNotEqual(Node(3, 1, 10), Node(5, 1, 10))

    def testComparing03(self):
        self.assertLess(Node(2, 1, 10), Node(9, 1, 10))

    def testComparing04(self):
        self.assertLessEqual(Node(4, 1, 10), Node(4, 1, 10))

    def testComparing05(self):
        self.assertLessEqual(Node(4, 1, 10), Node(6, 1, 10))

    def testComparing06(self):
        self.assertGreater(Node(9, 1, 10), Node(2, 1, 10))

    def testComparing07(self):
        self.assertGreaterEqual(Node(4, 1, 10), Node(4, 1, 10))

    def testComparing08(self):
        self.assertGreaterEqual(Node(8, 1, 10), Node(3, 1, 10))

    def testComparing09_min(self):
        i = [0]

        def assert_min(expected_min_value: int, values: {int}):
            self.assertEqual(expected_min_value,
                             min([Node(value, -9000, 9000) for value in values]).value,
                             msg=f"Test {i}")

        for node_values in [[2, 5, 6, 8, 9], [9, 2, 6, 5, 8]]:
            assert_min(min(node_values), node_values)

        random.seed(1337)

        for _ in range(100):
            node_values = set(random.randint(40, 9000) for _ in range(200))
            assert_min(min(node_values), node_values)
