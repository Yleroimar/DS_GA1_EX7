from tests.testing_utils.asserts import AddedAsserts

from utils.ring import Ring


class TestRingLookups(AddedAsserts):

    def testLookups01_outside(self):
        self.assertRingLookup(
                Ring(1, 10, [2, 5, 9], []), 20
        )

    def testLookups99_example1(self):
        self.assertRingLookup(
                Ring(1, 100, [5, 17, 22, 56, 71, 89, 92], [(5, 56), (5, 71), (22, 89)]),
                key=69, starting_value=17,
                expected_node=71, expected_requests=3
        )

    def testLookups99_example2(self):
        self.assertRingLookup(
                Ring(1, 100, [5, 17, 22, 56, 71, 89, 92], [(5, 56), (5, 71), (22, 89)]),
                key=87, starting_value=None,
                expected_node=89, expected_requests=2
        )

    # TODO: add more tests?
