from tests.testing_utils.asserts import *


class TestRingLookups(AddedAsserts):

    def testLookups001_outside1(self):
        self.assertRingLookup(
            init_ring(1, 10, [2, 5, 9], []), key=20
        )


    def testLookups002_outside2(self):
        self.assertRingLookup(
            init_ring(2, 10, [3, 5, 9], []), key=1
        )


    def testLookups101_simple1(self):
        self.assertRingLookup(
            init_ring(1, 10, [2, 5, 9], []),
            key=3,
            expected_node=5, expected_requests=1
        )


    def testLookups102_simple2(self):
        self.assertRingLookup(
            init_ring(1, 10, [2, 5, 9], []),
            key=10,
            expected_node=2, expected_requests=0
        )


    def testLookups201_past1(self):
        self.assertRingLookup(
            init_ring(1, 100,
                      [5, 7, 17, 22, 56, 71, 89, 92],
                      [(56, 92), (56, 17), (92, 7), (92, 17)]),
            key=6, starting_value=56,
            expected_node=7, expected_requests=2
        )


    def testLookups202_past2(self):
        self.assertRingLookup(
            init_ring(1, 100,
                      [5, 7, 17, 22, 56, 71, 89, 92],
                      [(56, 92), (56, 17), (92, 17)]),
            key=6, starting_value=56,
            expected_node=7, expected_requests=3
        )


    def testLookups301_ahead1(self):
        self.assertRingLookup(
            init_ring(1, 100,
                      [5, 7, 17, 22, 56, 71, 89, 92],
                      [(56, 92), (56, 17), (92, 17)]),
            key=6, starting_value=56,
            expected_node=7, expected_requests=3
        )


    def testLookups302_ahead2(self):
        self.assertRingLookup(
            init_ring(1, 100,
                      [5, 7, 17, 22, 56, 71, 89, 92],
                      [(56, 92), (56, 7)]),
            key=15, starting_value=56,
            expected_node=17, expected_requests=2
        )


    def testLookups999_example1(self):
        self.assertRingLookup(
            init_ring(1, 100, [5, 17, 22, 56, 71, 89, 92], [(5, 56), (5, 71), (22, 89)]),
            key=69, starting_value=17,
            expected_node=71, expected_requests=3
        )


    def testLookups999_example2(self):
        self.assertRingLookup(
            init_ring(1, 100, [5, 17, 22, 56, 71, 89, 92], [(5, 56), (5, 71), (22, 89)]),
            key=87, starting_value=None,
            expected_node=89, expected_requests=2
        )

    # TODO: add more tests?
