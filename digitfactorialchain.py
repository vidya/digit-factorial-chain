"""
Problem Description
https://projecteuler.net/problem=74

Digit factorial chains
Problem 74 The number 145 is well known
for the property that the sum of the
factorial of its digits is equal to 145:

    1! + 4! + 5! = 1 + 24 + 120 = 145

Perhaps less well known is 169, in that
it produces the longest chain of numbers
that link back to 169; it turns out that
there are only three such loops that exist:

    169 → 363601 → 1454 → 169
    871 → 45361 → 871
    872 → 45362 → 872

It is not difficult to prove that EVERY
starting number will eventually get stuck
in a loop. For example,

    69 → 363600 → 1454 → 169 → 363601 (→ 1454)
    78 → 45360 → 871 → 45361 (→ 871)
    540 → 145 (→ 145)

Starting with 69 produces a chain of five
non-repeating terms, but the longest
non-repeating chain with a starting number
below one million is sixty terms.

How many chains, with a starting number
below one million, contain exactly sixty
non-repeating terms?
"""

"""
    Answer = 402
"""
import threading
from threading import Thread


class DigitFactorialChain(Thread):
    nums_computed = {}
    len_60_count = 0

    threading_lock = threading.Lock()

    digit_facts = [
        1,

        1,
        1 * 2,
        1 * 2 * 3,

        1 * 2 * 3 * 4,
        1 * 2 * 3 * 4 * 5,
        1 * 2 * 3 * 4 * 5 * 6,

        1 * 2 * 3 * 4 * 5 * 6 * 7,
        1 * 2 * 3 * 4 * 5 * 6 * 7 * 8,
        1 * 2 * 3 * 4 * 5 * 6 * 7 * 8 * 9,
    ]

    @classmethod
    def init_nums_computed(cls):
        cls.nums_computed = {}
        cls.len_60_count = 0

    def __init__(self, start_num):
        super(DigitFactorialChain, self).__init__()
        self.daemon = True
        self.cancelled = False

        self.snum = start_num
        self.factorial_chain = []

    def digit_fact_sum(self, num):
        return sum([self.digit_facts[int(d)] for d in str(num)])

    @property
    def fact_chain_len(self):
        cls = self.__class__

        if self.snum in cls.nums_computed:
            return cls.nums_computed[self.snum]

        fc = [self.snum]
        while True:
            dfs_num = self.digit_fact_sum(fc[-1])
            if dfs_num in fc:
                break

            fc.append(dfs_num)

        self.factorial_chain = fc
        len_fc = len(fc)

        cls.threading_lock.acquire()
        for n in fc:
            cls.nums_computed[n] = len_fc

        if len_fc == 60:
            cls.len_60_count += 1
        cls.threading_lock.release()

        return len_fc

    def run(self):
        cls = self.__class__

        if not self.snum in cls.nums_computed:
            cls.nums_computed[self.snum] = self.fact_chain_len

        return cls.nums_computed[self.snum]


class ThreadCompute:
    def __init__(self, max_num):
        self.max_num = max_num

    @staticmethod
    def thread_compute():
        snum = 0
        max_num = 1000000
        max_threads = 1000

        while snum in range(max_num):
            threads = []

            for n in range(max_threads):
                t = DigitFactorialChain(snum)

                t.start()
                threads.append(t)

                snum += 1

            for t in threads:
                t.join()

