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

''' Miscellaneous support code.

    Most code that is here in the C++ implementation is redundant, or else
    implemented in a more sensible location.
'''


def PCG_128BIT_CONSTANT(high, low):
    ''' Some members of the PCG library use 128-bit math.

        This is not a problem for Python at all. But still provide this
        method of constructing literals, for compatibility.
    '''
    return high << 64 | low

# C++ iostreams don't exist. Instead, the Engine class supports __reduce__.

def unxorshift(x, bits, shift):
    ''' XorShifts are invertable, but they are someting of a pain to invert.

        This function backs them out.  It's used by the whacky "inside out"
        generator defined later.
    '''
    itype = type(x)
    if 2*shift >= bits:
        return x ^ (x >> shift)
    lowmask1 = (itype.ONE << (bits - shift*2)) - 1
    highmask1 = ~lowmask1
    top1 = x
    bottom1 = x & lowmask1
    top1 ^= top1 >> shift
    top1 &= highmask1
    x = top1 | bottom1
    lowmask2 = (itype.ONE << (bits - shift)) - 1
    bottom2 = x & lowmask2
    bottom2 = unxorshift(bottom2, bits - shift, shift)
    bottom2 &= lowmask1
    return top1 | bottom2

# rotl and rotr are implemented on the ints.* classes

# C++-style seed sequences don't exist. Instead, the seed must always be
# a bytestring of appropriate length, or defaults to urandom.

def bounded_rand(rng, upper_bound):
    if not 0 < upper_bound:
        raise ValueError('Bound must be positive!')
    if not upper_bound <= rng.MAX:
        # TODO: remove this limitation (not possible in C++ :P)
        raise ValueError('Bound must (currently) fit in result size!')
    rtype = type(rng.MAX)
    assert rng.MAX == rtype.MAX

    threshold = (rtype.MOD - upper_bound) % upper_bound
    while True:
        r = rng()
        if r >= threshold:
            return int(r) % upper_bound

def shuffle(arr, rng):
    count = len(arr)
    while count > 1:
        chosen = bounded_rand(rng, count)
        count -= 1
        arr[chosen], arr[count] = arr[count], arr[chosen]

# static_arbitrary_seed appears to be used by *nobody* at all,
# and what would it even mean in Python?

# printable_typename is unneeded in Python, repr() does a good job already.
