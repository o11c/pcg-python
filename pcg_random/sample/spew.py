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

''' This program outputs 215 GB of random bits (binary data).  This is
    about the same as the total output of random.org in its 15 year history.
    The code uses 1.25e-8 of the period, and chooses an arbitrary stream from
    2^64 streams.

    Typical usage:
        python3 -m pcg_random.sample.spew | hexdump -C | less
'''

from pcg_random import pcg32_fast

import numpy as np
import sys


def main():
    rng = pcg32_fast()
    print(rng, '\n', sep='', file=sys.stderr)

    BUFFER_SIZE = 1024 * 128
    buffer = np.ndarray(BUFFER_SIZE, dtype=np.uint32)
    ROUNDS = 215 * 1024**3 // buffer.nbytes

    for i in range(ROUNDS):
        for vi in range(len(buffer)):
            buffer[vi] = rng()
        # buffer.tofile() fails on nonseekable files for some reason
        sys.stdout.buffer.write(buffer.tobytes())


if __name__ == '__main__':
    main()
