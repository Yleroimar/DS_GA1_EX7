from tests.testing_utils.asserts import *


class TestRingShortcuts(AddedAsserts):

    # def testShortcuts00_selfLoopA(self):
    #     """ Just a highlighting test. Should this be allowed? """
    #     self.assertRingShortcut(
    #             init_ring(1, 10, [2, 4, 7, 9], [(9, 7)]),
    #             4, 4,
    #             "2:, S-4, NS-7",
    #             "4:4, S-7, NS-9",
    #             "7:, S-9, NS-2",
    #             "9:7, S-2, NS-4",
    #     )

    def testShortcuts00_selfLoopB(self):
        """ Just a highlighting test. Assuming self-loops are discarded. """
        self.assertRingShortcut(
                init_ring(1, 10, [2, 4, 7, 9], [(9, 7)]),
                4, 4,
                "2:, S-4, NS-7",
                "4:, S-7, NS-9",
                "7:, S-9, NS-2",
                "9:7, S-2, NS-4",
        )

    def testShortcuts01_startNotPresent(self):
        self.assertRingShortcut(
            init_ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(22, 89)]),
            5, 22,
            "7:, S-17, NS-22",
            "17:, S-22, NS-56",
            "22:89, S-56, NS-71",
            "56:, S-71, NS-89",
            "71:, S-89, NS-92",
            "89:, S-92, NS-7",
            "92:, S-7, NS-17",
        )

    def testShortcuts02_endNotPresent(self):
        self.assertRingShortcut(
            init_ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(22, 89)]),
            7, 90,
            "7:, S-17, NS-22",
            "17:, S-22, NS-56",
            "22:89, S-56, NS-71",
            "56:, S-71, NS-89",
            "71:, S-89, NS-92",
            "89:, S-92, NS-7",
            "92:, S-7, NS-17",
        )

    def testShortcuts03_startAndEndNotPresent(self):
        self.assertRingShortcut(
            init_ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(22, 89)]),
            20, 90,
            "7:, S-17, NS-22",
            "17:, S-22, NS-56",
            "22:89, S-56, NS-71",
            "56:, S-71, NS-89",
            "71:, S-89, NS-92",
            "89:, S-92, NS-7",
            "92:, S-7, NS-17",
        )

    def testShortcuts04_startIsBiggerThanEnd(self):
        self.assertRingShortcut(
            init_ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(22, 89)]),
            92, 22,
            "7:, S-17, NS-22",
            "17:, S-22, NS-56",
            "22:89, S-56, NS-71",
            "56:, S-71, NS-89",
            "71:, S-89, NS-92",
            "89:, S-92, NS-7",
            "92:22, S-7, NS-17",
        )

    def testShortcuts05_alreadyHadTheShortcut(self):
        self.assertRingShortcut(
            init_ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(22, 89)]),
            22, 89,
            "7:, S-17, NS-22",
            "17:, S-22, NS-56",
            "22:89, S-56, NS-71",
            "56:, S-71, NS-89",
            "71:, S-89, NS-92",
            "89:, S-92, NS-7",
            "92:, S-7, NS-17",
        )

    def testShortcuts06_multipleFingers(self):
        self.assertRingShortcut(
            init_ring(1, 100, [7, 17, 22, 56, 71, 89, 92], [(22, 89)]),
            22, 92,
            "7:, S-17, NS-22",
            "17:, S-22, NS-56",
            "22:89,92, S-56, NS-71",
            "56:, S-71, NS-89",
            "71:, S-89, NS-92",
            "89:, S-92, NS-7",
            "92:, S-7, NS-17",
        )

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
