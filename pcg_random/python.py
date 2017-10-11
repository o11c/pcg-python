# PCG Random Number Generation for C++ (ported to Python)
#
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

''' Standard python interface.
'''

import random
from .pcg_detail import AbstractEngine
from .pcg_engines import setseq_xsh_rr_64_32 as pcg32


class PcgRandom(random.Random):
    ''' Wrap an engine using the C++ interface in the Python interface.
    '''
    def __new__(cls, *args, **kwargs):
        # random.Random does initialization in __new__ rather than in
        # __init__. Our `engine` arg confuses it, so drop the arguments.
        return super().__new__(cls)

    def __init__(self, engine=pcg32, *seed_args, **seed_kwargs):
        if not isinstance(engine, AbstractEngine):
            self._engine = engine(*seed_args, **seed_kwargs)
        else:
            assert not seed_args and not seed_kwargs
            self._engine = engine

    def seed(self, *seed_args, **seed_kwargs):
        self._engine.seed(*seed_args, **seed_kwargs)

    def getstate(self):
        return self._engine.__reduce__()

    def setstate(self, state):
        c, a = state
        self._engine = c(*a)

    def getrandbits(self, k):
        assert isinstance(k, int) and k >= 0
        BITS_PER_CALL = self._engine.result_type.BITS
        shift = 0
        rv = 0
        while k >= BITS_PER_CALL:
            rv |= int(self._engine()) << shift
            shift += BITS_PER_CALL
            k -= BITS_PER_CALL
        if k:
            rv |= (int(self._engine()) % (1 << k)) << shift
        return rv

    def random(self):
        # Floating-point division of integers is hard to do correctly.
        # (Python does it right, however.)
        #
        # As a testcase, 5722605049457177600 / 15454911254934987586
        # should be 0.37027744482388164, not 0.3702774448238817
        #
        # However, other than underflow, dividing by powers of 2 is safe
        # in any language.

        # The int-to-float conversion rounds to nearest, but correct
        # result rely on truncation. Consider if the RNG produced 2**64-1.
        # (There are other problems if addition is used on the result)
        # UNSAFE: return self.getrandbits(64) / 2**64
        return self.getrandbits(53) / 2**53
