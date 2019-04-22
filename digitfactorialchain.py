import threading
from threading import Thread
import queue

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


class DigitFactorialChain(Thread):
    nums_computed = {}
    len_60_count = 0

    shared_area_lock = threading.Lock()

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

    num_str_fact_sum = {}
    num_fact_sum = []

    @classmethod
    def init_shared_area(cls):
        cls.nums_computed = {}
        cls.len_60_count = 0

        for n in range(1000):
            s = sum([cls.digit_facts[int(d)]
                     for d in str(n)])
            cls.num_fact_sum.append(s)

        for n in range(1000):
            ns = "%03d" % n
            cls.num_str_fact_sum[n] = sum([cls.digit_facts[int(d)]
                                           for d in ns])

    @classmethod
    def update_shared_area(cls, fact_sum_chain):
        cls.shared_area_lock.acquire()

        for n in fact_sum_chain:
            cls.nums_computed[n] = True

        if len(fact_sum_chain) == 60:
            cls.len_60_count += 1

        cls.shared_area_lock.release()

    def __init__(self, start_num):
        super(DigitFactorialChain, self).__init__()
        self.daemon = True
        self.cancelled = False

        self.start_num = start_num

    def digit_fact_sum(self, num):
        if num < 1000:
            return self.num_fact_sum[num]

        n1, n2 = divmod(num, 1000)
        return self.num_fact_sum[n1] + self.num_str_fact_sum[n2]

    def calc_fact_chain_len(self):
        fc = {}
        num = self.start_num
        while num not in fc:
            fc[num] = True
            num = self.digit_fact_sum(num)

        self.__class__.update_shared_area(fc)
        return len(fc)

    def run(self):
        self.calc_fact_chain_len()


class ThreadCompute:
    q = queue.Queue()

    @staticmethod
    def worker():
        q = ThreadCompute.q
        while True:
            num = q.get()
            if num is None:
                break

            DigitFactorialChain(num).calc_fact_chain_len()
            q.task_done()

    @staticmethod
    def use_worker_threads(max_num):
        thread_count = 20
        threads = [threading.Thread(target=ThreadCompute.worker)
                   for _ in range(thread_count)]

        for t in threads:
            t.start()

        q = ThreadCompute.q
        for num in range(max_num):
            q.put(num)

        # block until all numbers have been retrieved from
        # the queue and processed
        q.join()

        # stop workers
        for i in range(thread_count):
            q.put(None)

        # wait for all the threads to run to completion
        for t in threads:
            t.join()


