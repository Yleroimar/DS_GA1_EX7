from tests.testing_utils.asserts import AddedAsserts

from utils.ring import Ring


class TestRingShortcuts(AddedAsserts):

    def testShortcuts99_example(self):
        self.assertRingShortcut(
                Ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(22, 89)]),
                7, 22,
                "7:22, S-17, NS-22",
                "17:, S-22, NS-56",
                "22:89, S-56, NS-71",
                "56:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-7",
                "92:, S-7, NS-17",
        )

    # TODO: add more tests?
