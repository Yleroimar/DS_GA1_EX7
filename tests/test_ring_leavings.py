from tests.testing_utils.asserts import *


class TestRingLeavings(AddedAsserts):

    @unittest.expectedFailure
    def testLeaving00_fail(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 9], []),
            2,
            "2:, S-2, NS-2"
        )


    def testLeaving01_cannotLeave(self):
        self.assertRingLeave(
            init_ring(1, 10, [2], []),
            2,
            "2:, S-2, NS-2"
        )


    def testLeaving02_cannotLeave(self):
        self.assertRingLeave(
            init_ring(1, 10, [2], []),
            9,
            "2:, S-2, NS-2"
        )


    def testLeaving03_fewRemain1(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 9], []),
            2,
            "9:, S-9, NS-9"
        )


    def testLeaving04_fewRemain1(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 9], []),
            9,
            "2:, S-2, NS-2"
        )


    def testLeaving05_fewRemain2(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 5, 9], []),
            2,
            "5:, S-9, NS-5",
            "9:, S-5, NS-9"
        )


    def testLeaving06_fewRemain2(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 5, 9], []),
            5,
            "2:, S-9, NS-2",
            "9:, S-2, NS-9"
        )


    def testLeaving07_fewRemain2(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 5, 9], []),
            9,
            "2:, S-5, NS-2",
            "5:, S-2, NS-5"
        )


    def testLeaving08_fewRemain3(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 4, 7, 9], []),
            2,
            "4:, S-7, NS-9",
            "7:, S-9, NS-4",
            "9:, S-4, NS-7"
        )


    def testLeaving09_fewRemain3(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 4, 7, 9], []),
            4,
            "2:, S-7, NS-9",
            "7:, S-9, NS-2",
            "9:, S-2, NS-7"
        )


    def testLeaving10_fewRemain3(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 4, 7, 9], []),
            7,
            "2:, S-4, NS-9",
            "4:, S-9, NS-2",
            "9:, S-2, NS-4"
        )


    def testLeaving11_fewRemain3(self):
        self.assertRingLeave(
            init_ring(1, 10, [2, 4, 7, 9], []),
            9,
            "2:, S-4, NS-7",
            "4:, S-7, NS-2",
            "7:, S-2, NS-4"
        )


    def testLeaving12_fewRemain4(self):
        self.assertRingLeave(
            init_ring(1, 20, [2, 7, 10, 14, 19], []),
            2,
            "7:, S-10, NS-14",
            "10:, S-14, NS-19",
            "14:, S-19, NS-7",
            "19:, S-7, NS-10"
        )


    def testLeaving13_fewRemain4(self):
        self.assertRingLeave(
            init_ring(1, 20, [2, 7, 10, 14, 19], []),
            7,
            "2:, S-10, NS-14",
            "10:, S-14, NS-19",
            "14:, S-19, NS-2",
            "19:, S-2, NS-10"
        )


    def testLeaving14_fewRemain4(self):
        self.assertRingLeave(
            init_ring(1, 20, [2, 7, 10, 14, 19], []),
            10,
            "2:, S-7, NS-14",
            "7:, S-14, NS-19",
            "14:, S-19, NS-2",
            "19:, S-2, NS-7"
        )


    def testLeaving15_fewRemain4(self):
        self.assertRingLeave(
            init_ring(1, 20, [2, 7, 10, 14, 19], []),
            14,
            "2:, S-7, NS-10",
            "7:, S-10, NS-19",
            "10:, S-19, NS-2",
            "19:, S-2, NS-7"
        )


    def testLeaving16_fewRemain4(self):
        self.assertRingLeave(
            init_ring(1, 20, [2, 7, 10, 14, 19], []),
            19,
            "2:, S-7, NS-10",
            "7:, S-10, NS-14",
            "10:, S-14, NS-2",
            "14:, S-2, NS-7"
        )


    def testLeaving17_shortcuts(self):
        self.assertRingLeave(
            init_ring(1, 100, [10, 30, 50, 70, 90], [(50, 10), (50, 30), (30, 90)]),
            50,
            "10:, S-30, NS-70",
            "30:90, S-70, NS-90",
            "70:, S-90, NS-10",
            "90:, S-10, NS-30"
        )


    def testLeaving18_shortcuts(self):
        self.assertRingLeave(
            init_ring(1, 100, [10, 30, 50, 70, 90], [(50, 10), (50, 30), (10, 70)]),
            70,
            "10:, S-30, NS-50",
            "30:, S-50, NS-90",
            "50:10,30, S-90, NS-10",
            "90:, S-10, NS-30"
        )


    def testLeaving99_example(self):
        self.assertRingLeave(
            init_ring(1, 100, [5, 7, 17, 22, 56, 71, 89, 92], [(5, 56), (5, 71), (22, 89)]),
            5,
            "7:, S-17, NS-22",
            "17:, S-22, NS-56",
            "22:89, S-56, NS-71",
            "56:, S-71, NS-89",
            "71:, S-89, NS-92",
            "89:, S-92, NS-7",
            "92:, S-7, NS-17"
        )
