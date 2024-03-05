from collatz import collatz_iter


def test_collatz_iter():
    n = 9
    expected = [28, 14, 7, 22, 11, 34, 17, 52,
                26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    actual = list(collatz_iter(n))

    assert (expected == actual)
