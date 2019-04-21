from digitfactorialchain.digitfactorialchain import DigitFactorialChain
from digitfactorialchain.digitfactorialchain import ThreadCompute


def test_1_basic():
    DigitFactorialChain.init_nums_computed()

    t = DigitFactorialChain(169)

    t.start()
    t.join()

    expected = 3
    result = len(DigitFactorialChain.nums_computed)

    assert result == expected


def test_2_basic():
    DigitFactorialChain.init_nums_computed()

    t = DigitFactorialChain(69)

    t.start()
    t.join()

    expected = 5
    result = len(DigitFactorialChain.nums_computed)

    assert result == expected
    assert True


def test_3_basic():
    DigitFactorialChain.init_nums_computed()

    t = DigitFactorialChain(871)

    t.start()
    t.join()

    expected = 2
    result = len(DigitFactorialChain.nums_computed)

    assert result == expected


def test_4_basic():
    DigitFactorialChain.init_nums_computed()

    t = DigitFactorialChain(871)

    t.start()
    t.join()

    expected = 2
    result = len(DigitFactorialChain.nums_computed)

    assert result == expected


def test_5_basic():
    DigitFactorialChain.init_nums_computed()

    max_num = 1000000

    ThreadCompute(max_num).thread_compute()

    len_count_60 = DigitFactorialChain.len_60_count
    expected = 402

    print("(max_num, len_count_60) = ({}, {})".format(max_num, len_count_60))

    assert len_count_60 == expected

