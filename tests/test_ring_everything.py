from tests.testing_utils.asserts import *

from utils.ring import Ring


class TestRingEverything(AddedAsserts):

    def testEverything99_example(self):
        ks_min = 1
        ks_max = 100

        key_set = init_key_set_constructor(ks_min, ks_max)

        ring = init_ring(ks_min, ks_max,
                         [5, 56, 22, 17, 89, 71, 92, 110],
                         [(5, 56), (5, 71), (22, 89)])

        self.assertRing(
                ring,
                "5:56,71, S-17, NS-22",
                "17:, S-22, NS-56",
                "22:89, S-56, NS-71",
                "56:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-5",
                "92:, S-5, NS-17"
        )

        self.assertRingKeys(ring, [
            (5, key_set(93, 5)),
            (17, key_set(6, 17)),
            (22, key_set(18, 22)),
            (56, key_set(23, 56)),
            (71, key_set(57, 71)),
            (89, key_set(72, 89)),
            (92, key_set(90, 92)),
        ])

        self.assertRingLookup(ring, key=69, starting_value=17,
                              expected_node=71, expected_requests=3)

        self.assertRingLookup(ring, key=87, starting_value=None,
                              expected_node=89, expected_requests=2)

        self.assertRingJoin(
                ring, 7,
                "5:56,71, S-7, NS-17",
                "7:, S-17, NS-22",
                "17:, S-22, NS-56",
                "22:89, S-56, NS-71",
                "56:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-5",
                "92:, S-5, NS-7",
        )

        self.assertRingKeys(ring, [
            (5, key_set(93, 5)),
            (7, key_set(6, 7)),
            (17, key_set(8, 17)),
            (22, key_set(18, 22)),
            (56, key_set(23, 56)),
            (71, key_set(57, 71)),
            (89, key_set(72, 89)),
            (92, key_set(90, 92)),
        ])

        self.assertRingLeave(
                ring, 5,
                "7:, S-17, NS-22",
                "17:, S-22, NS-56",
                "22:89, S-56, NS-71",
                "56:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-7",
                "92:, S-7, NS-17"
        )

        self.assertRingKeys(ring, [
            (7, key_set(93, 7)),
            (17, key_set(8, 17)),
            (22, key_set(18, 22)),
            (56, key_set(23, 56)),
            (71, key_set(57, 71)),
            (89, key_set(72, 89)),
            (92, key_set(90, 92)),
        ])

        self.assertRingShortcut(
                ring, 7, 22,
                "7:22, S-17, NS-22",
                "17:, S-22, NS-56",
                "22:89, S-56, NS-71",
                "56:, S-71, NS-89",
                "71:, S-89, NS-92",
                "89:, S-92, NS-7",
                "92:, S-7, NS-17",
        )

        self.assertRingKeys(ring, [
            (7, key_set(93, 7)),
            (17, key_set(8, 17)),
            (22, key_set(18, 22)),
            (56, key_set(23, 56)),
            (71, key_set(57, 71)),
            (89, key_set(72, 89)),
            (92, key_set(90, 92)),
        ])

        # self.assertRingRemove(
        #         ring, [17, 22, 56],
        #         "7:, S-71, NS-89",
        #         "71:, S-89, NS-92",
        #         "89:, S-92, NS-7",
        #         "92:, S-7, NS-71"
        # )
        #
        # self.assertRingKeys(ring, [
        #     (7, key_set(93, 7)),
        #     (71, key_set(8, 71)),
        #     (89, key_set(72, 89)),
        #     (92, key_set(90, 92)),
        # ])
