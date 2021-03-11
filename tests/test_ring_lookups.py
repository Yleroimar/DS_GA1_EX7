from tests.testing_utils.asserts import *


class TestRingLookups(AddedAsserts):

    def testLookups01_outside1(self):
        self.assertRingLookup(
                init_ring(1, 10, [2, 5, 9], []), 20
        )

    def testLookups02_outside2(self):
        self.assertRingLookup(
                init_ring(2, 10, [3, 5, 9], []), 1
        )

    def testLookups03_past1(self):
        self.assertRingLookup(
                init_ring(1, 100,
                          [5, 7, 17, 22, 56, 71, 89, 92],
                          [(56, 92), (56, 17), (92, 7), (92, 17)]),
                key=6, starting_value=56,
                expected_node=7, expected_requests=2
        )

    def testLookups04_past2(self):
        self.assertRingLookup(
                init_ring(1, 100,
                          [5, 7, 17, 22, 56, 71, 89, 92],
                          [(56, 92), (56, 17), (92, 17)]),
                key=6, starting_value=56,
                expected_node=7, expected_requests=3
        )

    def testLookups05_ahead1(self):
        self.assertRingLookup(
                init_ring(1, 100,
                          [5, 7, 17, 22, 56, 71, 89, 92],
                          [(56, 92), (56, 17), (92, 17)]),
                key=6, starting_value=56,
                expected_node=7, expected_requests=3
        )

    def testLookups99_example1(self):
        self.assertRingLookup(
                init_ring(1, 100, [5, 17, 22, 56, 71, 89, 92], [(5, 56), (5, 71), (22, 89)]),
                key=69, starting_value=17,
                expected_node=71, expected_requests=3
        )

    def testLookups99_example2(self):
        self.assertRingLookup(
                init_ring(1, 100, [5, 17, 22, 56, 71, 89, 92], [(5, 56), (5, 71), (22, 89)]),
                key=87, starting_value=None,
                expected_node=89, expected_requests=2
        )

    # TODO: add more tests?
