from tests.testing_utils.asserts import *


class TestNodeKeys(AddedAsserts):

    def testKeys99_example1(self):
        ks_min = 1
        ks_max = 100

        ks_constructor = init_key_set_constructor(ks_min, ks_max)

        ring = init_ring(ks_min, ks_max,
                         [5, 17, 22, 56, 71, 89, 92],
                         [(5, 56), (5, 71), (22, 89)])

        self.assertRingKeys(ring, [
            (5, ks_constructor(93, 5)),
            (17, ks_constructor(6, 17)),
            (22, ks_constructor(18, 22)),
            (56, ks_constructor(23, 56)),
            (71, ks_constructor(57, 71)),
            (89, ks_constructor(72, 89)),
            (92, ks_constructor(90, 92)),
        ])

    def testKeys99_example2(self):
        ks_min = 1
        ks_max = 100

        key_set = init_key_set_constructor(ks_min, ks_max)

        ring = init_ring(ks_min, ks_max,
                         [5, 7, 17, 22, 56, 71, 89, 92],
                         [(5, 56), (5, 71), (22, 89)])

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

    def testKeys99_example3(self):
        ks_min = 1
        ks_max = 100

        key_set = init_key_set_constructor(ks_min, ks_max)

        ring = init_ring(ks_min, ks_max,
                         [7, 17, 22, 56, 71, 89, 92],
                         [(22, 89)])

        self.assertRingKeys(ring, [
            (7, key_set(93, 7)),
            (17, key_set(8, 17)),
            (22, key_set(18, 22)),
            (56, key_set(23, 56)),
            (71, key_set(57, 71)),
            (89, key_set(72, 89)),
            (92, key_set(90, 92)),
        ])

    def testKeys99_example4(self):
        ks_min = 1
        ks_max = 100

        key_set = init_key_set_constructor(ks_min, ks_max)

        ring = init_ring(ks_min, ks_max, [7, 71, 89, 92], [])

        self.assertRingKeys(ring, [
            (7, key_set(93, 7)),
            (71, key_set(8, 71)),
            (89, key_set(72, 89)),
            (92, key_set(90, 92)),
        ])
