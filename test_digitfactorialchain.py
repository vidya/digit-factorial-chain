from digitfactorialchain.digitfactorialchain import DigitFactorialChain
from digitfactorialchain.digitfactorialchain import ThreadCompute


def test_1_basic():
    DigitFactorialChain.init_shared_area()

    dfc = DigitFactorialChain(169)

    expected = 3
    result = dfc.calc_fact_chain_len()

    assert result == expected


def test_2_basic():
    DigitFactorialChain.init_shared_area()

    dfc = DigitFactorialChain(69)

    expected = 5
    result = dfc.calc_fact_chain_len()

    assert result == expected
    assert True


def test_3_basic():
    DigitFactorialChain.init_shared_area()

    dfc = DigitFactorialChain(871)

    expected = 2
    result = dfc.calc_fact_chain_len()

    assert result == expected


def test_4_basic():
    DigitFactorialChain.init_shared_area()

    dfc = DigitFactorialChain(872)

    expected = 2
    result = dfc.calc_fact_chain_len()

    assert result == expected


def test_5_basic():
    DigitFactorialChain.init_shared_area()

    max_num = 1000000

    ThreadCompute().use_worker_threads(max_num)

    len_count_60 = DigitFactorialChain.len_60_count
    expected = 402

    print("(max_num, len_count_60) = ({}, {})".format(max_num, len_count_60))

    assert len_count_60 == expected

