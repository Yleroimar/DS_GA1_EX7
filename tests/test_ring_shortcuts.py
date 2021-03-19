from tests.testing_utils.asserts import *


class TestRingShortcuts(AddedAsserts):

    # def testShortcuts00_selfLoop(self):
    #     """ Just a highlighting test. Should this be allowed? """
    #     self.assertRingShortcut(
    #             init_ring(1, 10, [2, 4, 7, 9], [(9, 7)]),
    #             4, 4,
    #             "2:, S-4, NS-7",
    #             "4:4, S-7, NS-9",
    #             "7:, S-9, NS-2",
    #             "9:7, S-2, NS-4",
    #     )

    def testShortcuts99_example(self):
        self.assertRingShortcut(
                init_ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(22, 89)]),
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
