import unittest

from tests.testing_utils.asserts import AddedAsserts

from utils.ring import Ring


class TestRingInits(AddedAsserts):
    @unittest.expectedFailure
    def testRingInit00_empty(self):
        self.assertRing(Ring(1, 10, [], []), "")

    def testRingInit01(self):
        self.assertRing(
                Ring(1, 10, [2, 9], []),
                "2:, S-9, NS-2",
                "9:, S-2, NS-9"
        )

    def testRingInit02(self):
        self.assertRing(
                Ring(1, 10, [0, 9], []),
                "9:, S-9, NS-9"
        )

    def testRingInit03(self):
        # EXTREME ABOUT KEY-SPACE LOWER-BOUND
        self.assertRing(
                Ring(1, 10, [1, 9], []),
                "1:, S-9, NS-1",
                "9:, S-1, NS-9"
        )

    def testRingInit04(self):
        self.assertRing(
                Ring(1, 10, [2, 11], []),
                "2:, S-2, NS-2"
        )

    def testRingInit05(self):
        # EXTREME ABOUT KEY-SPACE UPPER-BOUND
        self.assertRing(
                Ring(1, 10, [2, 10], []),
                "2:, S-10, NS-2",
                "10:, S-2, NS-10"
        )

    def testRingInit06(self):
        self.assertRing(
                Ring(1, 10, [2, 5, 6, 8, 9], [(5, 2), (9, 6), (9, 2)]),
                "2:, S-5, NS-6",
                "5:2, S-6, NS-8",
                "6:, S-8, NS-9",
                "8:, S-9, NS-2",
                "9:6,2, S-2, NS-5"
        )

    def testRingInit07(self):
        self.assertRing(
                Ring(1, 10, [2, 5, 9], []),
                "2:, S-5, NS-9",
                "5:, S-9, NS-2",
                "9:, S-2, NS-5"
        )

    def testRingInit99_example(self):
        self.assertRing(
                Ring(1, 100, [5, 17, 22, 56, 71, 89, 92], [(5, 56), (5, 71), (22, 89)]),
                "5:56,71, S-17, NS-22",
                "17:, S-22, NS-56",
                "22:89, S-56, NS-71",
                "56:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-5",
                "92:, S-5, NS-17"
        )
