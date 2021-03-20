import random

from tests.testing_utils.asserts import AddedAsserts
from src.distributed.node_ref import NodeRef


class TestNodeComparing(AddedAsserts):

    def testComparing01(self):
        self.assertEqual(NodeRef(5), NodeRef(5))


    def testComparing02(self):
        self.assertNotEqual(NodeRef(3), NodeRef(5))


    def testComparing03(self):
        self.assertLess(NodeRef(2), NodeRef(9))


    def testComparing04(self):
        self.assertLessEqual(NodeRef(4), NodeRef(4))


    def testComparing05(self):
        self.assertLessEqual(NodeRef(4), NodeRef(6))


    def testComparing06(self):
        self.assertGreater(NodeRef(9), NodeRef(2))


    def testComparing07(self):
        self.assertGreaterEqual(NodeRef(4), NodeRef(4))


    def testComparing08(self):
        self.assertGreaterEqual(NodeRef(8), NodeRef(3))


    def testComparing09_min(self):
        i = [0]


        def assert_min(expected_min_value: int, values: {int}):
            self.assertEqual(expected_min_value,
                             min([NodeRef(value) for value in values]).get_value(),
                             msg=f"Test {i}")


        for node_values in [[2, 5, 6, 8, 9], [9, 2, 6, 5, 8]]:
            assert_min(min(node_values), node_values)

        random.seed(1337)

        for _ in range(100):
            node_values = set(random.randint(40, 9000) for _ in range(200))
            assert_min(min(node_values), node_values)
