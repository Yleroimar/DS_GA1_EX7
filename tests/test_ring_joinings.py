from tests.testing_utils.asserts import AddedAsserts

from utils.ring import Ring


class TestRingJoins(AddedAsserts):

    def testJoins01(self):
        ring = Ring(1, 10, [5], [])

        self.assertRingJoin(
                ring, 2,
                "2:, S-5, NS-2",
                "5:, S-2, NS-5"
        )

        self.assertRingJoin(
                ring, 4,
                "2:, S-4, NS-5",
                "4:, S-5, NS-2",
                "5:, S-2, NS-4"
        )

    def testJoins02(self):
        ring = Ring(1, 10, [5], [])

        self.assertRingJoin(
                ring, 2,
                "2:, S-5, NS-2",
                "5:, S-2, NS-5"
        )

        self.assertRingJoin(
                ring, 8,
                "2:, S-5, NS-8",
                "5:, S-8, NS-2",
                "8:, S-2, NS-5"
        )

    def testJoins03(self):
        self.assertRingJoin(
                Ring(1, 10, [2, 5], []),
                4,
                "2:, S-4, NS-5",
                "4:, S-5, NS-2",
                "5:, S-2, NS-4"
        )

    def testJoins04(self):
        self.assertRingJoin(
                Ring(1, 10, [2, 5], []),
                8,
                "2:, S-5, NS-8",
                "5:, S-8, NS-2",
                "8:, S-2, NS-5"
        )

    def testJoins05(self):
        self.assertRingJoin(
                Ring(1, 10, [2, 4, 5], []),
                8,
                "2:, S-4, NS-5",
                "4:, S-5, NS-8",
                "5:, S-8, NS-2",
                "8:, S-2, NS-4"
        )

    def testJoins06(self):
        self.assertRingJoin(
                Ring(1, 10, [2, 5, 8], []),
                4,
                "2:, S-4, NS-5",
                "4:, S-5, NS-8",
                "5:, S-8, NS-2",
                "8:, S-2, NS-4"
        )

    def testJoins07(self):
        self.assertRingJoin(
                Ring(1, 10, [2, 4, 5, 8], []),
                9,
                "2:, S-4, NS-5",
                "4:, S-5, NS-8",
                "5:, S-8, NS-9",
                "8:, S-9, NS-2",
                "9:, S-2, NS-4"
        )

    def testJoins99(self):
        self.assertRingJoin(
                Ring(1, 10, [2, 3, 4, 5, 6, 7], []),
                8,
                "2:, S-3, NS-4",
                "3:, S-4, NS-5",
                "4:, S-5, NS-6",
                "5:, S-6, NS-7",
                "6:, S-7, NS-8",
                "7:, S-8, NS-2",
                "8:, S-2, NS-3"
        )

    def testJoins99_example(self):
        self.assertRingJoin(
                Ring(1, 100, [5, 17, 22, 56, 71, 89, 92], [(5, 56), (5, 71), (22, 89)]),
                7,
                "5:56,71, S-7, NS-17",
                "7:, S-17, NS-22",
                "17:, S-22, NS-56",
                "22:89, S-56, NS-71",
                "56:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-5",
                "92:, S-5, NS-7",
        )

    # TODO: add more tests?
