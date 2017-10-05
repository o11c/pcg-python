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

''' Actual implementation of the engine and plentiful supporting code.

    Warning for all who read this code: this is far from Pythonic.
    Similarity with the original C++ codebase is more important.

    Last updated for commit 0ca2e8ea6ba212bdfbc6219c2313c45917e34b8d
'''

import types

from .ints import *
from . import mixin
from . import pcg_extras
from .pointer import *


# The LCG generators need some constants to function.  This code lets you
# look up the constant by *type*.
#
# This code looks significantly different than the C++ version, but is
# still usable as a (dynamic) mixin.

default_multiplier_data = {}
class default_multiplier:
    def multiplier(self):
        return default_multiplier_data[self.itype]

default_increment_data = {}
class default_increment:
    def increment(self):
        return default_increment_data[self.itype]

def PCG_DEFINE_CONSTANT(type, kind, what, constant):
    dct = globals()['%s_%s_data' % (kind, what)]
    dct[type] = type(constant)

PCG_DEFINE_CONSTANT(uint8_t, 'default', 'multiplier', 141)
PCG_DEFINE_CONSTANT(uint8_t, 'default', 'increment', 77)

PCG_DEFINE_CONSTANT(uint16_t, 'default', 'multiplier', 12829)
PCG_DEFINE_CONSTANT(uint16_t, 'default', 'increment', 47989)

PCG_DEFINE_CONSTANT(uint32_t, 'default', 'multiplier', 747796405)
PCG_DEFINE_CONSTANT(uint32_t, 'default', 'increment', 2891336453)

PCG_DEFINE_CONSTANT(uint64_t, 'default', 'multiplier', 6364136223846793005)
PCG_DEFINE_CONSTANT(uint64_t, 'default', 'increment', 1442695040888963407)

PCG_DEFINE_CONSTANT(uint128_t, 'default', 'multiplier', pcg_extras.PCG_128BIT_CONSTANT(2549297995355413924, 4865540595714422341))
PCG_DEFINE_CONSTANT(uint128_t, 'default', 'increment', pcg_extras.PCG_128BIT_CONSTANT(6364136223846793005, 1442695040888963407))


# Each PCG generator is available in four variants, based on how it applies
# the additive constant for its underlying LCG; the variations are:
#
#     single stream   - all instances use the same fixed constant, thus
#                       the RNG always somewhere in same sequence
#     mcg             - adds zero, resulting in a single stream and reduced
#                       period
#     specific stream - the constant can be changed at any time, selecting
#                       a different random sequence
#     unique stream   - the constant is based on the memory addresss of the
#                       object, thus every RNG has its own unique sequence
#
# This variation is provided though mixin classes which define a function
# value called increment() that returns the nesessary additive constant.

class unique_stream:
    _is_mcg = False

    def set_stream(*args):
        raise TypeError('method not applicable')

    @property
    def state_type(self):
        return self.itype

    def increment(self):
        return self.itype(id(self) | 1)

    def stream(self):
        return self.increment() >> 1

    can_specify_stream = False

    def streams_pow2(self):
        return min(self.itype.BITS, uintptr_t.BITS) - 1


class no_stream: # mcg
    _is_mcg = True

    def set_stream(*args):
        raise TypeError('method not applicable')

    @property
    def state_type(self):
        return self.itype

    def increment(self):
        return self.itype.ZERO

    def stream(*args):
        raise TypeError('method not applicable')

    can_specify_stream = False

    def streams_pow2(self):
        return 0


class oneseq_stream (default_increment): # single stream
    _is_mcg = False

    def set_stream(*args):
        raise TypeError('method not applicable')

    @property
    def state_type(self):
        return self.itype

    def stream(self):
         return self.increment() >> 1

    can_specify_stream = False

    def streams_pow2(self):
        return 0


class specific_stream:
    _is_mcg = False

    @property
    def _inc(self):
        return default_increment_data[self.itype] # or constructor value

    @property
    def state_type(self):
        return self.itype

    @property
    def stream_state(self):
        return self.itype

    def increment(self):
        return self._inc

    def stream(self):
        return self._inc >> 1

    def set_stream(self, specific_seq):
        self._inc = specific_seq << 1 | 1

    can_specify_stream = True

    def streams_pow2(self):
        return self.itype.BITS - 1


class Engine:
    ''' This is where it all comes together.

        This class dynamically joins the three mixin classes which define
           - the LCG additive constant (the stream)
           - the LCG multiplier
           - the output function

        In addition, we specify the types of the LCG state and result,
        and whether to use the pre-advance version of the state for the
        output (increasing instruction-level parallelism) or the
        post-advance version (reducing register pressure). (This tradeoff
        doesn't really make sense for Python, but ... compatibility)

        Given the high level of parameterization and the original code's
        use of templates, parts of this code are ... interesting.
    '''

    def __init__(self,
            # template arguments
            xtype,
            itype,
            output_mixin,
            output_previous = True,
            stream_mixin = oneseq_stream,
            multiplier_mixin = default_multiplier,
            # instance arguments
            seed=None,
            stream_seed=None,
    ):
        # for easier pickling
        # (can't store instance arguments yet, since they change)
        self._template_arguments = (xtype, itype, output_mixin, output_previous, stream_mixin, multiplier_mixin)
        self.xtype = xtype
        self.itype = itype
        self.output_mixin = output_mixin
        self.output_previous = output_previous
        self.stream_mixin = stream_mixin
        self.multiplier_mixin = multiplier_mixin

        mixin.dynamic_mixin(self, output_mixin, protected=True)
        mixin.dynamic_mixin(self, stream_mixin)
        mixin.dynamic_mixin(self, multiplier_mixin, protected=True)

        # no need for *_stream_tag

        self.result_type = xtype
        self.state_type = itype

        self.MIN = self.result_type.ZERO
        self.MAX = self.result_type.MAX

        self.seed(seed, stream_seed)

    def seed(self, seed=None, stream_seed=None):
        if seed is False:
            assert stream_seed is None
            # prevent doing extra work seeding twice when using wrappers
            return
        elif seed is True:
            seed = None
        itype = self.itype
        if seed is None:
            # The C++ version defaults seed to itype(0xcafef00dd15ea5e5)
            # However, unwanted early construction isn't a thing in python,
            # so we default to seeding from /dev/urandom instead.
            seed = itype.urandom()
        elif not isinstance(seed, itype):
            # disallow int, since who knows how many real bits it has
            raise TypeError('Seed of wrong type!')
        else:
            # if seed was explicitly specified, don't urandom stream_seed.
            if stream_seed is None:
                stream_seed = False

        if stream_seed is None and self.can_specify_stream:
            stream_seed = itype.urandom()
        if stream_seed is not None and stream_seed is not False:
            if not self.can_specify_stream:
                raise TypeError('Stream mixin not seedable, but stream seed given!')
            elif isinstance(stream_seed, bool):
                if stream_seed:
                    stream_seed = None
            elif not isinstance(stream_seed, itype):
                raise TypeError('Stream seed of wrong type!')
        if stream_seed is not None and stream_seed is not False:
            # already checked that self.can_specify_stream
            # however, if only the main seed is passed, or if the
            # stream_seed is explicitly passed as False, use the default
            # for *now* (you can call set_stream later)..
            self.set_stream(stream_seed)

        if self._is_mcg:
            self._state = seed | 3
        else:
            # Note that this must come *after* self.set_stream(stream_seed)
            self._state = self._bump(seed + self.increment())

    def __repr__(self):
        args = list(self.pickle_args())
        for i, a in enumerate(args):
            if isinstance(a, type):
                args[i] = a.__qualname__
            else:
                args[i] = repr(a)
        return 'Engine(%s)' % ', '.join(args)

    def copy(self):
        return Engine(*self.pickle_args())

    def __reduce__(self):
        return (Engine, self.pickle_args())

    def pickle_args(self):
        return self._template_arguments + self._instance_args()

    def _instance_args(self):
        seed = getattr(self, '_state', False)
        if seed is False:
            return (seed, None)
        if not self._is_mcg:
            seed = self._unbump(seed) - self.increment()
        if self.can_specify_stream:
            return (seed, self.stream())
        else:
            return (seed, None)

    def compare_args(self):
        return (self._multiplier(), self.increment(), self._state)

    def _byte_sizeof(self):
        return self.itype.BYTES * (1 + self.can_specify_stream)

    def period_pow2(self):
        return self.state_type.BITS - 2*self._is_mcg

    def _bump(self, state):
        # simple version of _staticmethod_advance(delta=1)
        return state * self._multiplier() + self.increment()

    def _unbump(self, state):
        # this has to go the long way around :(
        # it's O(log n), where n is self.itype.BITS
        return self._staticmethod_advance(state, -1, self._multiplier(), self.increment())

    def _base_generate(self):
        rv = self._state = self._bump(self._state)
        return rv

    def _base_generate0(self):
        old_state = self._state
        self._state = self._bump(old_state)
        return old_state

    def __call__(self, upper_bound=None):
        if upper_bound is not None:
            return pcg_extras.bounded_rand(self, upper_bound)

        if self.output_previous:
            return self._output(self._base_generate0())
        else:
            return self._output(self._base_generate())

    # quasi-@staticmethod, but needs template arguments
    def _staticmethod_advance(self, state, delta, cur_mult, cur_plus):
        ''' efficient O(log n) version of n calls to _bump()

            The method used here is based on Brown, "Random Number Generation
            with Arbitrary Stride,", Transactions of the American Nuclear
            Society (Nov. 1994).  The algorithm is very similar to fast
            exponentiation.

            Even though delta is an unsigned integer, we can pass a
            signed integer to go backwards, it just goes "the long way round".
        '''
        itype = self.itype
        assert itype is type(state) is type(cur_mult) is type(cur_plus)
        delta = itype.coerce(delta)

        acc_mult = itype.ONE
        acc_plus = itype.ZERO
        while delta:
            if delta & 1:
                acc_mult *= cur_mult
                acc_plus = acc_plus*cur_mult + cur_plus
            cur_plus = (cur_mult+1)*cur_plus
            cur_mult *= cur_mult
            delta >>= 1
        return acc_mult * state + acc_plus

    # quasi-@staticmethod, but needs template arguments
    def _staticmethod_distance(self, cur_state, newstate, cur_mult, cur_plus, mask=-1):
        itype = self.itype
        assert itype is type(cur_state) is type(newstate) is type(cur_mult) is type(cur_plus)
        assert type(mask) in (itype, int)
        maybe_mcg_shift = 2 * self._is_mcg

        the_bit = itype.ONE << maybe_mcg_shift
        distance = itype.ZERO
        while (cur_state & mask) != (newstate & mask):
            if (cur_state & the_bit) != (newstate & the_bit):
                cur_state = cur_state * cur_mult + cur_plus
                distance |= the_bit
            assert (cur_state & the_bit) == (newstate & the_bit)
            the_bit <<= 1
            cur_plus = (cur_mult+1)*cur_plus
            cur_mult *= cur_mult
        return distance >> maybe_mcg_shift

    def _distance(self, newstate, mask=-1):
        return self._staticmethod_distance(self._state, newstate, self._multiplier(), self.increment(), mask)

    def advance(self, delta):
        self._state = self._staticmethod_advance(self._state, delta, self._multiplier(), self.increment())

    def backstep(self, delta):
        self.advance(-delta)

    discard = advance

    def wrapped(self):
        # For MCGs, the low order two bits never change. In this
        # implementation, we keep them fixed at 3 to make this test
        # easier.
        return 3 * self._is_mcg

    def __eq__(self, other):
        if not isinstance(other, Engine):
            return NotImplemented
        # When comparing for equality, Deliberately be sloppy.
        #return self.pickle_args() == other.pickle_args()
        return self.compare_args() == other.compare_args()

    def __sub__(self, other):
        if not isinstance(other, Engine):
            return NotImplemented
        assert self.stream_mixin is other.stream_mixin
        assert self.multiplier_mixin is other.multiplier_mixin
        return other._distance(self._state)

def oneseq_base(xtype, itype, output_mixin, output_previous=None, *seed_args, **seed_kwargs):
    if output_previous is None:
        output_previous = itype.BYTES <= 8
    rv = Engine(xtype, itype, output_mixin, output_previous, oneseq_stream, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def unique_base(xtype, itype, output_mixin, output_previous=None, *seed_args, **seed_kwargs):
    if output_previous is None:
        output_previous = itype.BYTES <= 8
    rv = Engine(xtype, itype, output_mixin, output_previous, unique_stream, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def setseq_base(xtype, itype, output_mixin, output_previous=None, *seed_args, **seed_kwargs):
    if output_previous is None:
        output_previous = itype.BYTES <= 8
    rv = Engine(xtype, itype, output_mixin, output_previous, specific_stream, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def mcg_base(xtype, itype, output_mixin, output_previous=None, *seed_args, **seed_kwargs):
    if output_previous is None:
        output_previous = itype.BYTES <= 8
    rv = Engine(xtype, itype, output_mixin, output_previous, no_stream, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv


# OUTPUT FUNCTIONS.
#
# These are the core of the PCG generation scheme.  They specify how to
# turn the base LCG's internal state into the output value of the final
# generator.
#
# They're implemented as mixin classes.
#
# All of the classes have code that is written to allow it to be applied
# at *arbitrary* bit sizes, although in practice they'll only be used at
# standard sizes supported by C++.

class xsh_rs_mixin:
    ''' XSH RS -- high xorshift, followed by a random shift

        Fast.  A good performer.
    '''

    def output(self, internal):
        itype = self.itype
        xtype = self.xtype
        bits = itype.BITS
        xtypebits = xtype.BITS
        sparebits = bits - xtypebits
        opbits = (
                5 if sparebits-5 >= 64 else
                4 if sparebits-4 >= 32 else
                3 if sparebits-3 >= 16 else
                2 if sparebits-2 >= 4 else
                1 if sparebits-1 >= 1 else
                0
        )
        mask = (1 << opbits) - 1
        maxrandshift = mask
        topspare = opbits
        bottomspare = sparebits - topspare
        xshift = topspare + (xtypebits+maxrandshift)//2
        rshift = int(internal >> (bits - opbits)) & mask if opbits else 0
        internal ^= internal >> xshift
        result = xtype(internal >> (bottomspare - maxrandshift + rshift))
        return result

class xsh_rr_mixin:
    ''' XSH RR -- high xorshift, followed by a random rotate

        Fast.  A good performer.  Slightly better statistically than XSH RS.
    '''

    def output(self, internal):
        itype = self.itype
        xtype = self.xtype
        bits = itype.BITS
        xtypebits = xtype.BITS
        sparebits = bits - xtypebits
        wantedopbits = (
                7 if xtypebits >= 128 else
                6 if xtypebits >= 64 else
                5 if xtypebits >= 32 else
                4 if xtypebits >= 16 else
                3
        )
        opbits = min(sparebits, wantedopbits)
        amplifier = wantedopbits - opbits
        mask = (1 << opbits) - 1
        topspare = opbits
        bottomspare = sparebits - topspare
        xshift = (topspare + xtypebits)//2
        rot = int(internal >> (bits - opbits)) & mask if opbits else 0
        amprot = (rot << amplifier) & mask
        internal ^= internal >> xshift
        result = xtype(internal >> bottomspare)
        result = result.rotr(amprot)
        return result

class rxs_mixin:
    ''' RXS -- random xorshift
    '''

    def output(self, internal):
        itype = self.itype
        xtype = self.xtype
        bits = itype.BITS
        xtypebits = xtype.BITS
        shift = bits - xtypebits
        extrashift = (xtypebits - shift)//2
        rshift = (
                (internal >> (bits - 6)) & 63 if shift > 64+8 else
                (internal >> (bits - 5)) & 31 if shift > 32+4 else
                (internal >> (bits - 4)) & 15 if shift > 16+2 else
                (internal >> (bits - 3)) & 7 if shift > 8+1 else
                (internal >> (bits - 2)) & 3 if shift > 4+1 else
                (internal >> (bits - 1)) & 1 if shift > 2+1 else
                0
        )
        internal ^= internal >> (shift + extrashift - rshift)
        result = xtype(internal >> rshift)
        return result


# don't need the classes for these two
mcg_multiplier_data = {}
mcg_unmultiplier_data = {}

PCG_DEFINE_CONSTANT(uint8_t, 'mcg', 'multiplier', 217)
PCG_DEFINE_CONSTANT(uint8_t, 'mcg', 'unmultiplier', 105)

PCG_DEFINE_CONSTANT(uint16_t, 'mcg', 'multiplier', 62169)
PCG_DEFINE_CONSTANT(uint16_t, 'mcg', 'unmultiplier', 28009)

PCG_DEFINE_CONSTANT(uint32_t, 'mcg', 'multiplier', 277803737)
PCG_DEFINE_CONSTANT(uint32_t, 'mcg', 'unmultiplier', 2897767785)

PCG_DEFINE_CONSTANT(uint64_t, 'mcg', 'multiplier', 12605985483714917081)
PCG_DEFINE_CONSTANT(uint64_t, 'mcg', 'unmultiplier', 15009553638781119849)

PCG_DEFINE_CONSTANT(uint128_t, 'mcg', 'multiplier', pcg_extras.PCG_128BIT_CONSTANT(17766728186571221404, 12605985483714917081))
PCG_DEFINE_CONSTANT(uint128_t, 'mcg', 'unmultiplier', pcg_extras.PCG_128BIT_CONSTANT(14422606686972528997, 15009553638781119849))

class rxs_m_xs_mixin:
    ''' RXS M XS -- random xorshift, mcg multiply, fixed xorshift

        The most statistically powerful generator, but all those steps
        make it slower than some of the others.  We give it the rottenest jobs.

        Because it's usually used in contexts where the state type and the
        result type are the same, it is a permutation and is thus invertable.
        We thus provide a function to invert it.  This function is used to
        for the "inside out" generator used by the extended generator.
    '''

    def output(self, internal):
        xtype = self.xtype
        itype = self.itype
        xtypebits = xtype.BITS
        bits = itype.BITS
        opbits = (
                6 if xtypebits >= 128 else
                5 if xtypebits >= 64 else
                4 if xtypebits >= 32 else
                3 if xtypebits >= 16 else
                2
        )
        shift = bits - xtypebits
        mask = (1 << opbits) - 1
        rshift = int(internal >> (bits - opbits)) & mask if opbits else 0
        internal ^= internal >> (opbits + rshift)
        internal *= mcg_multiplier_data[itype]
        result = xtype(internal >> shift)
        result ^= result >> ((2*xtypebits+2)//3)
        return result

    def unoutput(self, internal):
        itype = self.itype
        assert itype is self.xtype
        bits = itype.BITS
        opbits = (
                6 if bits >= 128 else
                5 if bits >= 64 else
                4 if bits >= 32 else
                3 if bits >= 16 else
                2
        )
        mask = (1 << opbits) - 1

        internal = unxorshift(internal, bits, (2*bits+2)//3)

        internal *= mcg_unmultiplier_data[itype]

        rshift = int(internal >> (bits - opbits)) & mask if opbits else 0
        internal = unxorshift(internal, bits, opbits + rshift)

        return internal

class rxs_m_mixin:
    ''' RXS M -- random xorshift, mcg multiply
    '''

    def output(self, internal):
        xtype = self.xtype
        itype = self.itype
        xtypebits = xtype.BITS
        bits = itype.BITS
        opbits = (
                6 if xtypebits >= 128 else
                5 if xtypebits >= 64 else
                4 if xtypebits >= 32 else
                3 if xtypebits >= 16 else
                2
        )
        shift = bits - xtypebits
        mask = (1 << opbits) - 1
        rshift = int(internal >> (bits - opbits)) & mask if opbits else 0
        internal ^= internal >> (opbits + rshift)
        internal *= mcg_multiplier_data[itype]
        result = xtype(internal >> shift)
        return result

class xsl_rr_mixin:
    ''' XSL RR -- fixed xorshift (to low bits), random rotate

        Useful for 128-bit types that are split across two CPU registers.
    '''

    def output(self, internal):
        xtype = self.xtype
        itype = self.itype
        xtypebits = xtype.BITS
        bits = itype.BITS
        sparebits = bits - xtypebits
        wantedopbits = (
                7 if xtypebits >= 128 else
                6 if xtypebits >= 64 else
                5 if xtypebits >= 32 else
                4 if xtypebits >= 16 else
                3
        )
        opbits = min(sparebits, wantedopbits)
        amplifier = wantedopbits - opbits
        mask = (1 << opbits) - 1
        topspare = sparebits
        bottomspare = sparebits - topspare
        xshift = (topspare + xtypebits) // 2

        rot = int(internal >> (bits - opbits)) & mask if opbits else 0
        amprot = (rot << amplifier) & mask
        internal ^= internal >> xshift
        result = xtype(internal >> bottomspare)
        result = result.rotr(amprot)
        return result


halfsize_trait = {
        uint128_t: uint64_t,
        uint64_t: uint32_t,
        uint32_t: uint16_t,
        uint16_t: uint8_t,
}

class xsl_rr_rr_mixin:
    ''' XSL RR RR -- fixed xorshift (to low bits), random rotate (both parts)

        Useful for 128-bit types that are split across two CPU registers.
        If you really want an invertable 128-bit RNG, I guess this is the one.
    '''

    def output(self, internal):
        itype = self.itype
        assert itype is self.xtype
        htype = halfsize_trait[itype]
        htypebits = htype.BITS
        bits = itype.BITS
        sparebits = bits - htypebits
        assert sparebits == htypebits
        wantedopbits = (
                7 if htypebits >= 128 else
                6 if htypebits >= 64 else
                5 if htypebits >= 32 else
                4 if htypebits >= 16 else
                3
        )
        opbits = min(sparebits, wantedopbits)
        amplifier = wantedopbits - opbits
        mask = (1 << opbits) - 1
        topspare = sparebits
        xshift = (topspare + htypebits) // 2

        rot = int(internal >> (bits - opbits)) & mask if opbits else 0
        amprot = (rot << amplifier) & mask
        internal ^= internal >> xshift
        lowbits = htype(internal)
        lowbits = lowbits.rotr(amprot)
        highbits = htype(internal >> topspare)
        rot2 = int(lowbits) & mask
        amprot2 = (rot2 << amplifier) & mask
        highbits = highbits.rotr(amprot2)
        return (itype(highbits) << topspare) ^ itype(lowbits)

class xsh_mixin:
    ''' XSH -- fixed xorshift (to high bits)

        You shouldn't use this at 64-bits or less.
    '''
    def output(self, internal):
        xtype = self.xtype
        itype = self.itype
        xtypebits = xtype.BITS
        bits = itype.BITS
        sparebits = bits - xtypebits
        topspare = 0
        bottomspare = sparebits - topspare
        xshift = (topspare + xtypebits) // 2

        internal ^= internal >> xshift
        result = xtype(internal >> bottomspare)
        return result

class xsl_mixin:
    ''' XSL -- fixed xorshift (to low bits)

        You shouldn't use this at 64-bits or less.
    '''
    def output(self, internal):
        xtype = self.xtype
        itype = self.itype
        xtypebits = xtype.BITS
        bits = itype.BITS
        sparebits = bits - xtypebits
        topspare = sparebits
        bottomspare = sparebits - topspare
        xshift = (topspare + xtypebits) // 2

        internal ^= internal >> xshift
        result = xtype(internal >> bottomspare)
        return result

# ---- End of Output Functions ----


class inside_out:
    ''' Helper class for Extended.

        In the C++ version this uses private inheritance, but never
        creates instances. Note that the 'baseclass' here is actually the
        'extvalclass' in Extended.
    '''
    def __init__(self, baseclass):
        self.baseclass = baseclass
        self.result_type = baseclass.result_type
        self.state_type = baseclass.state_type
        if self.result_type is not self.state_type:
            raise TypeError("Require a RNG whose output function is a permutation")

    def external_step(self, ptr_randval, i):
        baseclass = self.baseclass
        state_type = self.state_type
        result_type = self.result_type

        state = baseclass.unoutput(ptr_randval.get())
        state = state * baseclass.multiplier() + baseclass.increment() + state_type(i*2)
        result = result_type(baseclass.output(state))
        ptr_randval.put(result)
        zero = state & state_type(3) if baseclass.is_mcg else state_type.ZERO
        return result == zero

    def external_advance(self, ptr_randval, i, delta, forwards=True):
        baseclass = self.baseclass
        state_type = self.state_type
        result_type = self.result_type

        state = baseclass.unoutput(ptr_randval.get())
        mult = baseclass.multiplier()
        inc = baseclass.increment() + state_type(i*2)
        zero = state & state_type(3) if baseclass.is_mcg else state_type.ZERO
        dist_to_zero = baseclass._staticmethod_distance(state, zero, mult, inc)
        if forwards:
            crosses_zero = dist_to_zero <= delta
        else:
            crosses_zero = (-dist_to_zero) <= delta
        if not forwards:
            delta = -delta
        state = baseclass._staticmethod_advance(state, delta, mult, inc)
        ptr_randval.put(baseclass.output(state))
        return crosses_zero

class Extended:
    ''' From small pieces, greater things are built.

        In the C++ version, this uses inheritance rather than composition.
    '''
    def __init__(self,
            # template arguments
            table_pow2,
            advance_pow2,
            baseclass,
            extvalclass,
            kdd=True,
            # instance arguments
            *seed_args, **seed_kwargs
    ):
        self._template_arguments = (table_pow2, advance_pow2, baseclass, extvalclass, kdd)
        # actually instances (eek!)
        baseclass = baseclass(seed=False) # seeded at end of __init__
        extvalclass = extvalclass(seed=False) # only quasi-staticmethods are used

        self.table_pow2 = table_pow2
        self.advance_pow2 = advance_pow2
        self.baseclass = baseclass
        self.extvalclass = extvalclass
        self.kdd = kdd

        # implicitly copied from base class
        self.itype = baseclass.itype
        self.xtype = baseclass.xtype
        self.MIN = baseclass.MIN
        self.MAX = baseclass.MAX
        self.streams_pow2 = baseclass.streams_pow2
        self.can_specify_stream = baseclass.can_specify_stream

        self.state_type = baseclass.state_type
        self.result_type = baseclass.result_type
        self.insideout = inside_out(extvalclass)

        self._rtypebits = self.result_type.BITS
        self._stypebits = self.state_type.BITS

        self._tick_limit_pow2 = 64

        self._table_size = 1 << table_pow2
        self._table_shift = self._stypebits - table_pow2
        self._table_mask = (self.state_type.ONE << table_pow2) - 1

        self._may_tick = advance_pow2 < self._stypebits and advance_pow2 < self._tick_limit_pow2
        self._tick_shift = self._stypebits - advance_pow2
        self._tick_mask = (self.state_type.ONE << advance_pow2) - 1 if self._may_tick else self.state_type.MAX

        self._may_tock = self._stypebits < self._tick_limit_pow2
        self.seed(*seed_args, **seed_kwargs)

    def seed(self, seed=None, stream_seed=None, data=None):
        if seed is False:
            assert stream_seed is None
            assert data is None
            return
        self.baseclass.seed(seed, stream_seed)
        if data is False:
            self._selfinit()
        else:
            if data is True:
                data = None
            self._datainit(data)

    def __repr__(self):
        args = list(self.pickle_args())
        for i, a in enumerate(args):
            if isinstance(a, (type, types.FunctionType)):
                args[i] = a.__qualname__
            else:
                args[i] = repr(a)
        return 'Extended(%s)' % ', '.join(args)

    def copy(self):
        return Extended(*self.pickle_args())

    def __reduce__(self):
        return (Extended, self.pickle_args())

    def pickle_args(self):
        return self._template_arguments + self._instance_args()

    def _instance_args(self):
        data = getattr(self, '_data', False)
        return self.baseclass._instance_args() + (data,)

    def _byte_sizeof(self):
        return self.baseclass._byte_sizeof() + self._table_size * self.result_type.BYTES

    def _advance_table(self, delta=None, isForwards=True):
        if delta is None:
            # overloaded 0-arg form
            carry = False
            for i in range(self._table_size):
                if carry:
                    carry = self.insideout.external_step(ItemPointer(data_, i), i+1)
                carry2 = self.insideout.external_step(ItemPointer(data_, i), i+1)
                carry = carry or carry2
            return

        base_state_t = self.baseclass.state_type
        ext_state_t = self.extvalclass.state_t
        basebits = base_state_t.BITS
        extbits = ext_state_t.BITS
        assert basebits <= extbits or advance_pow2 > 0, "Current implementation might overflow its carry"

        carry = base_state_t.ZERO
        for i in range(self._table_size):
            total_delta = carry + delta
            trunc_delta = ext_state_t(total_delta)
            if basebits > extbits:
                carry = total_delta >> extbits
            else:
                carry = base_state_t.ZERO
            carry += self.insideout.external_advance(ItemPointer(data_, i), i+1, trunc_delta, isForwards)

    def _get_extended_value(self):
        state = self.baseclass._state
        if self.kdd and self.baseclass._is_mcg:
            state >>= 2
        if self.kdd:
            index = state & self._table_mask
        else:
            index = state >> self._table_shift
        if self._may_tick:
            if self.kdd:
                tick = not (state & self._tick_mask)
            else:
                tick = not (state >> self._tick_shift)

            if tick:
                self.advance_table()
        if self._may_tock:
            tock = not state
            if tock:
                self.advance_table()
        return ItemPointer(self._data, index)

    def period_pow2(self):
        base_period = self.baseclass.period_pow2()
        ext_period = self.extvalclass.period_pow2()
        return base_period + self._table_size * ext_period

    def __call__(self, upper_bound=None):
        if upper_bound is not None:
            return pcg_extras.bounded_rand(self, upper_bound)

        rhs = self._get_extended_value().get()
        lhs = self.baseclass()
        return lhs ^ rhs
    def set(self, wanted):
        rhs = self._get_extended_value()
        lhs = self.baseclass()
        rhs.put(lhs ^ wanted)

    def advance(self, distance, forwards=True):
        state_type = self.state_type
        distance = state_type.coerce(distance)

        assert self.kdd, "Efficient advance is too hard for non-kdd extension. For a weak advance, cast to base class"
        zero = self.baseclass._state & state_type(3) if self.baseclass._is_mcg else state_type.ZERO
        if self._may_tick:
            ticks = distance >> self.advance_pow2
            adv_mask = self._tick_mask << (2 * self.baseclass._is_mcg)
            next_advance_distance = self.baseclass._distance(zero, adv_mask)
            if not forwards:
                next_advance_distance = (-next_advance_distance) & self._tick_mask
            if next_advance_distance < (distance & self._tick_mask):
                ticks += 1
            if ticks:
                self.advance_table(ticks, forwards)
        if forwards:
            if may_tock and self.distance(zero) <= distance:
                advance_table()
            self.baseclass.advance(distance)
        else:
            if self._may_tock and -(self.distance(zero)) <= distance:
                self.advance_table(state_type(1), False)
            self.baseclass.advance(-distance)
    def backstep(self, distance):
        self.advance(distance, False)

    def _selfinit(self):
        table_size = self._table_size
        # We need to fill the extended table with something, and we have
        # very little provided data, so we use the base generator to
        # produce values.  Although not ideal (use a seed sequence, folks!),
        # unexpected correlations are mitigated by
        #      - using XOR differences rather than the number directly
        #      - the way the table is accessed, its values *won't* be accessed
        #        in the same order the were written.
        #      - any strange correlations would only be apparent if we
        #        were to backstep the generator so that the base generator
        #        was generating the same values again
        lhs = self.baseclass()
        rhs = self.baseclass()
        xdiff = lhs - rhs
        self._data = [self.baseclass()^xdiff for _ in range(table_size)]

    def _datainit(self, data):
        table_size = self._table_size

        if data is None:
            data = self.result_type.urandom(count=table_size)
        else:
            data = list(data)
            if len(data) != table_size:
                raise ValueError('data of wrong length')
        self._data = data

    def __eq__(self, other):
        if not isinstance(other, Extended):
            return NotImplemented
        return self.baseclass == other.baseclass and self._data == other._data

    def __sub__(self, other):
        if not isinstance(other, Extended):
            return NotImplemented
        # Note: this is truncated!
        # But as long as you haven't advanced more than the baseclass's
        # period, it will be accurate.
        #
        # Unfortunately, I don't understand enough to figure out how to
        # detect if the appropriate number of wraps (0 or 1) have occurred.
        # It's *something* to do with the distance from zero ...
        return self.baseclass - other.baseclass
