from tests.testing_utils.asserts import *


class TestRingProceedingNode(AddedAsserts):

    def assertFindingProceedingNode(self, ring: LocalBackend, node_value: int, expected_value: int = None):
        self.skipTest("Deprecated")
        # proceeding = ring.find_proceeding_node(Node(node_value,
        #                                             ring.get_key_space_start(),
        #                                             ring.get_key_space_end()))
        #
        # if expected_value is None:
        #     self.assertIsNone(proceeding)
        #     return
        #
        # self.assertIsNotNone(proceeding)
        # self.assertEqual(expected_value, proceeding.value)

    # with node not added to ring

    def testProceedingNode01_notAdded1(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [10], []),
                                         node_value=5, expected_value=10)

    def testProceedingNode02_notAdded2(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [10], []),
                                         node_value=15, expected_value=10)

    def testProceedingNode03_notAdded3(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [10, 20], []),
                                         node_value=5, expected_value=10)

    def testProceedingNode04_notAdded4(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [10, 20], []),
                                         node_value=15, expected_value=20)

    def testProceedingNode05_notAdded5(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [10, 20], []),
                                         node_value=25, expected_value=10)

    # with node added to ring

    def testProceedingNode06_added1(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [5, 10], []),
                                         node_value=5, expected_value=10)

    def testProceedingNode07_added2(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [10, 15], []),
                                         node_value=15, expected_value=10)

    def testProceedingNode08_added3(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [5, 10, 20], []),
                                         node_value=5, expected_value=10)

    def testProceedingNode09_added4(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [10, 15, 20], []),
                                         node_value=15, expected_value=20)

    def testProceedingNode10_added5(self):
        self.assertFindingProceedingNode(init_ring(1, 30, [10, 20, 25], []),
                                         node_value=25, expected_value=10)
