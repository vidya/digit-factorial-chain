from digitfactorialchain.digitfactorialchain import DigitFactorialChain
from digitfactorialchain.digitfactorialchain import ThreadCompute


def test_1_basic():
    DigitFactorialChain.init_nums_computed()

    dfc = DigitFactorialChain(169)

    dfc.start()
    dfc.join()

    expected = 3
    result = dfc.fact_chain_len

    assert result == expected


def test_2_basic():
    DigitFactorialChain.init_nums_computed()

    dfc = DigitFactorialChain(69)

    dfc.start()
    dfc.join()

    expected = 5
    result = dfc.fact_chain_len

    assert result == expected
    assert True


def test_3_basic():
    DigitFactorialChain.init_nums_computed()

    dfc = DigitFactorialChain(871)

    dfc.start()
    dfc.join()

    expected = 2
    result = dfc.fact_chain_len

    assert result == expected


def test_4_basic():
    DigitFactorialChain.init_nums_computed()

    dfc = DigitFactorialChain(871)

    dfc.start()
    dfc.join()

    expected = 2
    result = dfc.fact_chain_len

    assert result == expected


def test_5_basic():
    DigitFactorialChain.init_nums_computed()

    max_num = 1000000

    ThreadCompute(max_num).thread_compute()

    len_count_60 = DigitFactorialChain.len_60_count
    expected = 402

    print("(max_num, len_count_60) = ({}, {})".format(max_num, len_count_60))

    assert len_count_60 == expected

