from collatz import build_tree, collatz_iter


def test_build_tree():
    m = 10
    expected = {2: 1,
                3: 10,
                4: 2,
                5: 16,
                6: 3,
                7: 22,
                8: 4,
                9: 28,
                10: 5,
                11: 34,
                13: 40,
                14: 7,
                16: 8,
                17: 52,
                20: 10,
                22: 11,
                26: 13,
                28: 14,
                34: 17,
                40: 20,
                52: 26}
    actual = build_tree(m)

    assert(expected == actual)


def test_collatz_iter():
    n = 9
    expected = [28, 14, 7, 22, 11, 34, 17, 52,
                26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    actual = list(collatz_iter(n))

    assert (expected == actual)
