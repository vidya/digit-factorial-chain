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

# subclass from Thread class
class DigitFactorialChain(Thread):
    compute_fact_sum_q = queue.Queue()

    # store the numbers whose factorial sums have been computed
    fact_sums_computed = {}

    # count numbers whose factorial sum chains have length 60
    chain_len_60_count = 0

    shared_area_lock = threading.Lock()

    # factorials of single digit numbers
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

    # store sums of factorials of digits for numbers < 1000
    # as a list
    onek_fact_sum = []

    # store sums of factorials of digits for numbers < 1000
    # as a dictionary with
    #
    #   (key=three_digit_string, value=sum_of_factorials_of_digits)
    #
    onek_str_fact_sum = {}

    @classmethod
    def init_shared_area(cls):
        cls.fact_sums_computed = {}
        cls.chain_len_60_count = 0

        for n in range(1000):
            s = sum([cls.digit_facts[int(d)]
                     for d in str(n)])

            cls.onek_fact_sum.append(s)

        for n in range(1000):
            ns = "%03d" % n
            cls.onek_str_fact_sum[n] = sum([cls.digit_facts[int(d)]
                                            for d in ns])

    # fact_sum_chain:
    #   chain of numbers obtained by repeatedly
    #   taking factorial sums
    @classmethod
    def update_shared_area(cls, fact_sum_chain):
        with cls.shared_area_lock:
            cls.fact_sums_computed = [True for _ in fact_sum_chain]

            if len(fact_sum_chain) == 60:
                cls.chain_len_60_count += 1

    def __init__(self, start_num):
        super(DigitFactorialChain, self).__init__()

        # make this a daemon thread, which will be automatically
        # killed when the main thread exits
        self.daemon = True
        self.cancelled = False

        self.start_num = start_num

    # calculate the sum of factorials of digits of num
    def digits_fact_sum(self, num):
        if num < 1000:
            return self.onek_fact_sum[num]

        q, r = divmod(num, 1000)
        return self.onek_fact_sum[q] + self.onek_str_fact_sum[r]

    # compute the factorial sum chain of start_num
    def fact_sum_chain(self):
        chain = []

        num = self.start_num
        while num not in chain:
            chain.append(num)
            num = self.digits_fact_sum(num)

        self.__class__.update_shared_area(chain)
        return chain

    def fact_sum_chain_len(self):
        return len(self.fact_sum_chain())

    def run(self):
        self.fact_sum_chain_len()

    @classmethod
    def worker(cls):
        q = cls.compute_fact_sum_q
        while True:
            num = q.get()
            if num is None:
                break

            DigitFactorialChain(num).fact_sum_chain()
            q.task_done()

    @classmethod
    def use_worker_threads(cls, max_num):
        cls.init_shared_area()

        # create twenty threads
        thread_count = 20
        threads = [threading.Thread(target=cls.worker)
                   for _ in range(thread_count)]

        # start the threads
        for t in threads:
            t.start()

        # enters numbers into the compute queue
        for num in range(max_num):
            cls.compute_fact_sum_q.put(num)

        # block until all numbers have been retrieved from
        # the queue and processed
        cls.compute_fact_sum_q.join()

        # stop workers
        for i in range(thread_count):
            cls.compute_fact_sum_q.put(None)

        # wait for all the threads to run to completion
        for t in threads:
            t.join()

        return cls.chain_len_60_count

