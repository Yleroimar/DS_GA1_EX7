from tests.testing_utils.asserts import AddedAsserts

from utils.ring import Ring


class TestRingRemoves(AddedAsserts):

    def testRemoves01_single(self):
        self.assertRingRemove(
                Ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(7, 22), (22, 89)]),
                [17],
                "7:22, S-22, NS-56",
                "22:89, S-56, NS-71",
                "56:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-7",
                "92:, S-7, NS-22"
        )

    def testRemoves02_tooMany(self):
        self.assertRingRemove(
                Ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(7, 22), (22, 89)]),
                [7, 17, 22, 56, 71, 89, 92],
                "7:22, S-17, NS-22",
                "17:, S-22, NS-56",
                "22:89, S-56, NS-71",
                "56:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-7",
                "92:, S-7, NS-17"
        )

    def testRemoves03_tooMany(self):
        self.assertRingRemove(
                Ring(1, 100, [7, 22, 89], [(7, 22), (22, 89)]),
                [7, 17, 22, 56, 71, 89, 92],
                "7:22, S-22, NS-89",
                "22:89, S-89, NS-7",
                "89:, S-7, NS-22"
        )

    def testRemoves04_duplicates1(self):
        self.assertRingRemove(
                Ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(7, 22), (22, 89)]),
                [56, 71, 89, 56],
                "7:22, S-17, NS-22",
                "17:, S-22, NS-92",
                "22:, S-92, NS-7",
                "92:, S-7, NS-17"
        )

    def testRemoves05_duplicates2(self):
        self.assertRingRemove(
                Ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(7, 22), (22, 89)]),
                [56, 71, 56, 89, 56, 56, 56, 56, 56, 56, 56],
                "7:22, S-17, NS-22",
                "17:, S-22, NS-92",
                "22:, S-92, NS-7",
                "92:, S-7, NS-17"
        )

    # @unittest.expectedFailure

    def testRemoves99_example(self):
        self.assertRingRemove(
                Ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(7, 22), (22, 89)]),
                [17, 22, 56],
                "7:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-7",
                "92:, S-7, NS-71"
        )

    # TODO: add more tests?
