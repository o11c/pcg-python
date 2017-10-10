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

''' This program behaves like the spew program, the only difference is that
    after 1 MB of output, the output gets "interesting" for a brief while.
    See make-partytrick.cpp for more details.
     *
    Typical usage:
        python3 -m pcg_random.sample.use_partytrick | hexdump -C | less

'''

from pcg_random import pcg32_k64

import numpy as np
import sys


def main():
    rng = pcg32_k64(seed=False)
    rng.seed(
            # different init than C++ due to different serialization
            # C++ serializes the internal state directly; python unwinds
            # to produce usable __init__ arguments.
            rng.itype(212842618354962723),
            rng.itype(1751662123863039415),
            [
                rng.xtype(i) for i in [
                103238831, 665891259, 1902651333, 4073047566, 368781010, 3371458373, 3520911659, 1176018374, 1290944887, 2479283234, 2214499777, 3287447736, 4241043352, 2808175048, 83300271, 162496091, 3372211384, 3773661488, 3842517107, 154403914, 1983905875, 185363760, 3574548828, 4259275054, 2055322655, 3183516320, 3827707798, 2358810643, 3947601356, 1518701804, 2987610801, 4256672123, 243420444, 2418646926, 1593945712, 3293969771, 1047458160, 4148325853, 4134598831, 813996594, 2374617805, 712898811, 2110551176, 233031372, 1753202862, 281911517, 1950853967, 3790278509, 4176603202, 4256155456, 1413186342, 1718872307, 2898301505, 1732438719, 622306094, 366401535, 2963949396, 2676833081, 98878999, 999895120, 425860638, 4096143638, 4063627507, 2566817785
            ]])
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
