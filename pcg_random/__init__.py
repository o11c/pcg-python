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

''' Pure python implementation of *full* (matching C++) pcg_random facilities.

    The emphasis is on completeness and correctness, not speed.

    The API should usually be very similar, except templates are flattened.

    This top-level module contains the convenience wrappers you should
    usually use. Additional wrappers are found in the pcg_engines module.
    Rarely, if ever, do you need the pcg_detail.Engine class directly.
'''

from . import pcg_extras, pcg_detail, pcg_engines
from .pcg_detail import AbstractEngine, Engine, Extended
from .python import PcgRandom


pcg32 = pcg_engines.setseq_xsh_rr_64_32
pcg32_oneseq = pcg_engines.oneseq_xsh_rr_64_32
pcg32_unique = pcg_engines.unique_xsh_rr_64_32
pcg32_fast = pcg_engines.mcg_xsh_rs_64_32

pcg64 = pcg_engines.setseq_xsl_rr_128_64
pcg64_oneseq = pcg_engines.oneseq_xsl_rr_128_64
pcg64_unique = pcg_engines.unique_xsl_rr_128_64
pcg64_fast = pcg_engines.mcg_xsl_rr_128_64

pcg8_once_insecure = pcg_engines.setseq_rxs_m_xs_8_8
pcg16_once_insecure = pcg_engines.setseq_rxs_m_xs_16_16
pcg32_once_insecure = pcg_engines.setseq_rxs_m_xs_32_32
pcg64_once_insecure = pcg_engines.setseq_rxs_m_xs_64_64
pcg128_once_insecure = pcg_engines.setseq_xsl_rr_rr_128_128

pcg8_oneseq_once_insecure = pcg_engines.oneseq_rxs_m_xs_8_8
pcg16_oneseq_once_insecure = pcg_engines.oneseq_rxs_m_xs_16_16
pcg32_oneseq_once_insecure = pcg_engines.oneseq_rxs_m_xs_32_32
pcg64_oneseq_once_insecure = pcg_engines.oneseq_rxs_m_xs_64_64
pcg128_oneseq_once_insecure = pcg_engines.oneseq_xsl_rr_rr_128_128


# These two extended RNGs provide two-dimensionally equidistributed
# 32-bit generators.  pcg32_k2_fast occupies the same space as pcg64,
# and can be called twice to generate 64 bits, but does not required
# 128-bit math; on 32-bit systems, it's faster than pcg64 as well.

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsh_rr_64_32)
def pcg32_k2(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsh_rr_64_32(1, 16, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsh_rs_64_32)
def pcg32_k2_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsh_rs_64_32(1, 32, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv


# These eight extended RNGs have about as much state as arc4random
#
#  - the k variants are k-dimensionally equidistributed
#  - the c variants offer better crypographic security
#
# (just how good the cryptographic security is is an open question)

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsh_rr_64_32)
def pcg32_k64(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsh_rr_64_32(6, 16, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_mcg_xsh_rs_64_32)
def pcg32_k64_oneseq(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_mcg_xsh_rs_64_32(6, 32, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsh_rs_64_32)
def pcg32_k64_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsh_rs_64_32(6, 32, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsh_rr_64_32)
def pcg32_c64(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsh_rr_64_32(6, 16, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsh_rs_64_32)
def pcg32_c64_oneseq(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsh_rs_64_32(6, 32, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_mcg_xsh_rs_64_32)
def pcg32_c64_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_mcg_xsh_rs_64_32(6, 32, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsl_rr_128_64)
def pcg64_k32(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsl_rr_128_64(5, 16, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsl_rr_128_64)
def pcg64_k32_oneseq(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsl_rr_128_64(5, 128, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_mcg_xsl_rr_128_64)
def pcg64_k32_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_mcg_xsl_rr_128_64(5, 128, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsl_rr_128_64)
def pcg64_c32(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsl_rr_128_64(5, 16, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsl_rr_128_64)
def pcg64_c32_oneseq(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsl_rr_128_64(5, 128, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_mcg_xsl_rr_128_64)
def pcg64_c32_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_mcg_xsl_rr_128_64(5, 128, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv


# These eight extended RNGs have more state than the Mersenne twister
#
#  - the k variants are k-dimensionally equidistributed
#  - the c variants offer better crypographic security
#
# (just how good the cryptographic security is is an open question)

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsh_rr_64_32)
def pcg32_k1024(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsh_rr_64_32(10, 16, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsh_rs_64_32)
def pcg32_k1024_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsh_rs_64_32(10, 32, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsh_rr_64_32)
def pcg32_c1024(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsh_rr_64_32(10, 16, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsh_rs_64_32)
def pcg32_c1024_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsh_rs_64_32(10, 32, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsl_rr_128_64)
def pcg64_k1024(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsl_rr_128_64(10, 16, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsl_rr_128_64)
def pcg64_k1024_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsl_rr_128_64(10, 128, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsl_rr_128_64)
def pcg64_c1024(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsl_rr_128_64(10, 16, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsl_rr_128_64)
def pcg64_c1024_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsl_rr_128_64(10, 128, False, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv


# These generators have an insanely huge period (2^524352), and is suitable
# for silly party tricks, such as dumping out 64 KB ZIP files at an arbitrary
# point in the future.   [Actually, over the full period of the generator, it
# will produce every 64 KB ZIP file 2^64 times!]

@pcg_engines._alias(wrap=pcg_engines.ext_setseq_xsh_rr_64_32)
def pcg32_k16384(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_setseq_xsh_rr_64_32(14, 16, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
@pcg_engines._alias(wrap=pcg_engines.ext_oneseq_xsh_rs_64_32)
def pcg32_k16384_fast(*seed_args, **seed_kwargs):
    rv = pcg_engines.ext_oneseq_xsh_rs_64_32(14, 32, True, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
