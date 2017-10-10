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

''' Produce a histogram of a normal distribution.
'''

import collections

from pcg_random import PcgRandom


def main():
    # Make a random number engine (seeded from /dev/urandom)
    rng = PcgRandom()

    # Choose a random mean between 1 and 6
    mean = rng.randint(1, 6)
    print("Randomly-chosen mean:", mean)

    # Generate a normal distribution around that mean
    def normal_dist(rng):
        return rng.normalvariate(mean, 2)

    # Make a copy of the RNG state to use later
    rng_checkpoint = rng._engine.copy()

    hist = collections.Counter()
    for n in range(10000):
        hist[round(normal_dist(rng))] += 1
    print("Normal distribution around ", mean, ":", sep='')
    for k, v in sorted(hist.items()):
        print(k, v//30 * '*')

    print("Required", int(rng._engine - rng_checkpoint), "random numbers.")


if __name__ == '__main__':
    main()
