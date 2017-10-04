# PCG Random Number Generation for C++ (ported to Python)
#
# Copyright 2014-2017 Melissa O'Neill <oneill@pcg-random.org>,
#                     and the PCG Project contributors.
# Copyright 2017 Ben Longbons <brlongbons@gmail.com>
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Licensed under the Apache License, Version 2.0 (provided in
# LICENSE-APACHE.txt and at http://www.apache.org/licenses/LICENSE-2.0)
# or under the MIT license (provided in LICENSE-MIT.txt and at
# http://opensource.org/licenses/MIT), at your option. This file may not
# be copied, modified, or distributed except according to those terms.
#
# Distributed on an "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, either
# express or implied.  See your chosen license for details.
#
# For additional information about the PCG random number generation scheme,
# visit http://www.pcg-random.org/.

''' Integration tests
'''

import pcg_random
from pcg_random.ints import *
from pcg_random import pcg_extras

import io
import pkg_resources
import pytest


class TestEngine:
    def test_pcg8_once_insecure(self):
        do_pcg_test(RNG='pcg8_once_insecure', TWO_ARG_INIT=True)
    def test_pcg8_oneseq_once_insecure(self):
        do_pcg_test(RNG='pcg8_oneseq_once_insecure', TWO_ARG_INIT=False)
    def test_pcg16_once_insecure(self):
        do_pcg_test(RNG='pcg16_once_insecure', TWO_ARG_INIT=True)
    def test_pcg16_oneseq_once_insecure(self):
        do_pcg_test(RNG='pcg16_oneseq_once_insecure', TWO_ARG_INIT=False)
    def test_pcg32(self):
        do_pcg_test(RNG='pcg32', TWO_ARG_INIT=True)
    @pytest.mark.xfail
    def test_pcg32_c1024(self):
        do_pcg_test(RNG='pcg32_c1024', TWO_ARG_INIT=True, advance=False)
    @pytest.mark.xfail
    def test_pcg32_c1024_fast(self):
        do_pcg_test(RNG='pcg32_c1024_fast', TWO_ARG_INIT=False, advance=False)
    @pytest.mark.xfail
    def test_pcg32_c64(self):
        do_pcg_test(RNG='pcg32_c64', TWO_ARG_INIT=True, advance=False)
    @pytest.mark.xfail
    def test_pcg32_c64_fast(self):
        do_pcg_test(RNG='pcg32_c64_fast', TWO_ARG_INIT=False, advance=False)
    @pytest.mark.xfail
    def test_pcg32_c64_oneseq(self):
        do_pcg_test(RNG='pcg32_c64_oneseq', TWO_ARG_INIT=False, advance=False)
    def test_pcg32_fast(self):
        do_pcg_test(RNG='pcg32_fast', TWO_ARG_INIT=False)
    @pytest.mark.xfail
    def test_pcg32_k1024(self):
        do_pcg_test(RNG='pcg32_k1024', TWO_ARG_INIT=True)
    @pytest.mark.xfail
    def test_pcg32_k1024_fast(self):
        do_pcg_test(RNG='pcg32_k1024_fast', TWO_ARG_INIT=False)
    @pytest.mark.xfail
    def test_pcg32_k16384(self):
        do_pcg_test(RNG='pcg32_k16384', TWO_ARG_INIT=True)
    @pytest.mark.xfail
    def test_pcg32_k16384_fast(self):
        do_pcg_test(RNG='pcg32_k16384_fast', TWO_ARG_INIT=False)
    @pytest.mark.xfail
    def test_pcg32_k2(self):
        do_pcg_test(RNG='pcg32_k2', TWO_ARG_INIT=True)
    @pytest.mark.xfail
    def test_pcg32_k2_fast(self):
        do_pcg_test(RNG='pcg32_k2_fast', TWO_ARG_INIT=False)
    @pytest.mark.xfail
    def test_pcg32_k64(self):
        do_pcg_test(RNG='pcg32_k64', TWO_ARG_INIT=True)
    @pytest.mark.xfail
    def test_pcg32_k64_fast(self):
        do_pcg_test(RNG='pcg32_k64_fast', TWO_ARG_INIT=False)
    @pytest.mark.xfail
    def test_pcg32_k64_oneseq(self):
        do_pcg_test(RNG='pcg32_k64_oneseq', TWO_ARG_INIT=False)
    def test_pcg32_once_insecure(self):
        do_pcg_test(RNG='pcg32_once_insecure', TWO_ARG_INIT=True)
    def test_pcg32_oneseq(self):
        do_pcg_test(RNG='pcg32_oneseq', TWO_ARG_INIT=False)
    def test_pcg32_oneseq_once_insecure(self):
        do_pcg_test(RNG='pcg32_oneseq_once_insecure', TWO_ARG_INIT=False)
    def test_pcg32_unique(self):
        # no output - unique
        pcg_test(RNG='pcg32_unique', TWO_ARG_INIT=False, advance=False, file=io.StringIO())
    def test_pcg64(self):
        do_pcg_test(RNG='pcg64', TWO_ARG_INIT=True)
    @pytest.mark.xfail
    def test_pcg64_c1024(self):
        do_pcg_test(RNG='pcg64_c1024', TWO_ARG_INIT=True, advance=False)
    @pytest.mark.xfail
    def test_pcg64_c1024_fast(self):
        do_pcg_test(RNG='pcg64_c1024_fast', TWO_ARG_INIT=False, advance=False)
    @pytest.mark.xfail
    def test_pcg64_c32(self):
        do_pcg_test(RNG='pcg64_c32', TWO_ARG_INIT=True, advance=False)
    @pytest.mark.xfail
    def test_pcg64_c32_fast(self):
        do_pcg_test(RNG='pcg64_c32_fast', TWO_ARG_INIT=False, advance=False)
    @pytest.mark.xfail
    def test_pcg64_c32_oneseq(self):
        do_pcg_test(RNG='pcg64_c32_oneseq', TWO_ARG_INIT=False, advance=False)
    def test_pcg64_fast(self):
        do_pcg_test(RNG='pcg64_fast', TWO_ARG_INIT=False)
    @pytest.mark.xfail
    def test_pcg64_k1024(self):
        do_pcg_test(RNG='pcg64_k1024', TWO_ARG_INIT=True)
    @pytest.mark.xfail
    def test_pcg64_k1024_fast(self):
        do_pcg_test(RNG='pcg64_k1024_fast', TWO_ARG_INIT=False)
    @pytest.mark.xfail
    def test_pcg64_k32(self):
        do_pcg_test(RNG='pcg64_k32', TWO_ARG_INIT=True)
    @pytest.mark.xfail
    def test_pcg64_k32_fast(self):
        do_pcg_test(RNG='pcg64_k32_fast', TWO_ARG_INIT=False)
    @pytest.mark.xfail
    def test_pcg64_k32_oneseq(self):
        do_pcg_test(RNG='pcg64_k32_oneseq', TWO_ARG_INIT=False)
    def test_pcg64_once_insecure(self):
        do_pcg_test(RNG='pcg64_once_insecure', TWO_ARG_INIT=True)
    def test_pcg64_oneseq(self):
        do_pcg_test(RNG='pcg64_oneseq', TWO_ARG_INIT=False)
    def test_pcg64_oneseq_once_insecure(self):
        do_pcg_test(RNG='pcg64_oneseq_once_insecure', TWO_ARG_INIT=False)
    def test_pcg64_unique(self):
        # no output - unique
        pcg_test(RNG='pcg64_unique', TWO_ARG_INIT=False, advance=False, file=io.StringIO())
    def test_pcg128_once_insecure(self):
        do_pcg_test(RNG='pcg128_once_insecure', TWO_ARG_INIT=True)
    def test_pcg128_oneseq_once_insecure(self):
        do_pcg_test(RNG='pcg128_oneseq_once_insecure', TWO_ARG_INIT=False)

def do_pcg_test(RNG, TWO_ARG_INIT, advance=True):
    out = io.StringIO()
    pcg_test(RNG, TWO_ARG_INIT, advance, file=out)
    actual = out.getvalue()
    expected = pkg_resources.resource_string(__name__, 'expected/check-%s.out' % RNG).decode('ascii')
    assert expected == actual

def pcg_test(RNG, TWO_ARG_INIT, advance=True, file=None):
    ''' This function is based on the demo program for the C generation schemes.

        It shows some basic generation tasks.
    '''
    if file is None:
        file = sys.stdout
    def p(*args):
        print(*args, sep='', end='', file=file)

    rounds = 5

    # Many of the generators can be initialized with two arguments; the second
    # one specifies the stream.

    rng = getattr(pcg_random, RNG)(seed=False)
    # Hm, maybe we should allow seeding from bare integers?
    # But then, this *is* just the test suite ...
    #
    # Alternative solution: set properties on the functions.
    if TWO_ARG_INIT:
        rng.seed(rng.itype(42), rng.itype(54))
    else:
        rng.seed(rng.itype(42))

    bits = rng.result_type.BITS
    how_many_nums = (
            14 if bits <= 8 else
            10 if bits <= 16 else
            6
    )
    wrap_nums_at = (
            2 if bits > 64 else
            3 if bits > 32 else
            how_many_nums
    )

    p(RNG, ":\n")
    p("      -  result:      ", bits, "-bit unsigned int\n")
    p("      -  period:      2^", rng.period_pow2())
    if rng.streams_pow2() > 0:
         p("   (* 2^", rng.streams_pow2(), " streams)")
    p("\n      -  size:        ", (rng.itype.BYTES * (1 + rng.can_specify_stream)), " bytes\n\n")

    for round in range(1, rounds+1):
        p("Round %d:\n" % round)

        # Make some N-bit numbers
        p('%4d' % bits, "bit:")
        for i in range(how_many_nums):
            if i and i % wrap_nums_at == 0:
                p("\n\t")
            p(" 0x%0*x" % (rng.result_type.NYBBLES, rng()))
        p('\n')

        if advance:
            p("  Again:")
            rng.backstep(6)
            for i in range(how_many_nums):
                if i and i % wrap_nums_at == 0:
                    p("\n\t")
                p(" 0x%0*x" % (rng.result_type.NYBBLES, rng()))
            p('\n')

        # Toss some coins
        p("  Coins: ")
        for i in range(65):
            p('TH'[rng(2)])
        p('\n')

        if advance:
            rng_copy = rng.copy()
        # Roll some dice
        p("  Rolls:")
        for i in range(33):
            p(" ", int(rng(6)) + 1)
        p('\n')
        if advance:
            p("   -->   rolling dice used ", int(rng - rng_copy), " random numbers\n")

        # Deal some cards using pcg_extras::shuffle, which follows
        # the algorithm for shuffling that most programmers would expect.
        # (It's unspecified how std::shuffle works.)
        number = 'A23456789TJQK'
        suit = 'hcds'
        cards = list(range(len(number) * len(suit)))
        pcg_extras.shuffle(cards, rng)

        # Output the shuffled deck
        p("  Cards:")
        for i, card in enumerate(cards, 1):
            p(" ", number[card // len(suit)], suit[card % len(suit)])
            if i % 22 == 0:
                p("\n\t")
        p('\n\n')
