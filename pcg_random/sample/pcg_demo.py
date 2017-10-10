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

''' This file is based on the demo program for the C generation schemes.

    It shows some basic generation tasks.
'''

RNG_STRING = 'pcg32'
from pcg_random import pcg32 as RNG, PcgRandom, pcg_extras
TWO_ARG_INIT = True


def main():
    # Read command-line options

    rounds = 5
    nondeterministic_seed = False

    from sys import argv
    argv = argv[1:]
    if argv and argv[0] == '-r':
        nondeterministic_seed = True
        argv = argv[1:]
    if argv:
        rounds = int(argv[0])

    # Many of the generators can be initialized with two arguments; the second
    # one specifies the stream.

    if nondeterministic_seed:
        rng = RNG()
    else:
        # Insecurely seeding is slightly painful. This is a Good Thing™.
        itype = RNG.itype
        if TWO_ARG_INIT:
            rng = RNG(itype(42), itype(54))
        else:
            rng = RNG(itype(42))


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

    print(RNG_STRING, ':', sep='')
    print("      -  result:      ", bits, "-bit unsigned int", sep='')
    print("      -  period:      2^", rng.period_pow2(), sep='', end='')
    if rng.streams_pow2():
         print("   (* 2^", rng.streams_pow2(), " streams)", sep='', end='')
    print("\n      -  size:        ", rng._byte_sizeof(), " bytes\n", sep='')

    for round in range(1, 5+1):
        print("Round ", round, ":", sep='')

        # Make some N-bit numbers
        print('%4d' % bits, "bit:", sep='', end='')
        for i in range(how_many_nums):
            if i and i % wrap_nums_at == 0:
                print('\n\t', end='')
            print(" 0x%0*x" % (rng.result_type.NYBBLES, rng()), end='')
        print()

        print("  Again:", end='')
        rng.backstep(6)
        for i in range(how_many_nums):
            if i and i % wrap_nums_at == 0:
                print('\n\t', end='')
            print(" 0x%0*x" % (rng.result_type.NYBBLES, rng()), end='')
        print()

        # Toss some coins
        print("  Coins: ", end='')
        for i in range(65):
            print('TH'[rng(2)], end='')
        print()

        rng_copy = rng.copy()
        # Roll some dice
        print("  Rolls:", end='')
        for i in range(33):
            print(' ', rng(6) + 1, sep='', end='')
        print("\n   -->   rolling dice used", int(rng - rng_copy), "random numbers")

        # Deal some cards using random.shuffle
        # It's unspecified *how* random.shuffle shuffles the cards, or how many
        # random numbers it will use to do so, so we call random.shuffle and
        # measure how good it is.  We won't use it for the final shuffle
        # to avoid platform-dependent output.
        rng_copy = rng.copy()
        number = 'A23456789TJQK'
        suit = 'hcds'
        cards = list(range(len(number) * len(suit)))
        PcgRandom(engine=rng).shuffle(cards)
        std_shuffle_steps = int(rng - rng_copy)

        # Restore RNG and deal again using pcg_extras.shuffle, which follows
        # the algorithm for shuffling that most programmers would expect.

        rng = rng_copy.copy()
        cards = list(range(len(number) * len(suit)))
        pcg_extras.shuffle(cards, rng)
        my_shuffle_steps = int(rng - rng_copy)

        # Output the shuffled deck
        print("  Cards:", end='')
        for i, card in enumerate(cards, 1):
            print(" ", number[card // len(suit)], suit[card % len(suit)], sep='', end='')
            if i % 22 == 0:
                print("\n\t", end='')

        # Output statistics about shuffling
        print("\n   -->   random.shuffle used", std_shuffle_steps, "random numbers", end='')
        if std_shuffle_steps > 52: # 1 spare because of the (rare) loop in bounded_rand
            # Python's `random` module sucks for a variety of reasons.
            # Here, it calls getrandbits() always with the minimum possible
            # value, and thus loops most of the time, rather than rarely.
            # Thus, values from 69 to 79 are commonly reported.
            print("\n\t -- that's", (std_shuffle_steps - 51), "more than we'd expect; inefficient implementation")
        print("\n   -->   pcg_extras.shuffle used", my_shuffle_steps, "random numbers\n")


if __name__ == '__main__':
    main()
