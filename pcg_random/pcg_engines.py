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

''' Mid-level convenience wrappers for various engine configurations.
'''

from .ints import *
from . import pcg_detail


# Predefined types for XSH RS

def oneseq_xsh_rs_16_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint8_t, uint16_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_xsh_rs_32_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint16_t, uint32_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_xsh_rs_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint32_t, uint64_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_xsh_rs_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint64_t, uint128_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def unique_xsh_rs_16_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint8_t, uint16_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_xsh_rs_32_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint16_t, uint32_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_xsh_rs_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint32_t, uint64_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_xsh_rs_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint64_t, uint128_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def setseq_xsh_rs_16_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint8_t, uint16_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_xsh_rs_32_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint16_t, uint32_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_xsh_rs_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint32_t, uint64_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_xsh_rs_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint64_t, uint128_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def mcg_xsh_rs_16_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint8_t, uint16_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def mcg_xsh_rs_32_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint16_t, uint32_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def mcg_xsh_rs_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint32_t, uint64_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def mcg_xsh_rs_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint64_t, uint128_t, pcg_detail.xsh_rs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv


# Predefined types for XSH RR

def oneseq_xsh_rr_16_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint8_t, uint16_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_xsh_rr_32_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint16_t, uint32_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_xsh_rr_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint32_t, uint64_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_xsh_rr_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint64_t, uint128_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def unique_xsh_rr_16_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint8_t, uint16_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_xsh_rr_32_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint16_t, uint32_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_xsh_rr_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint32_t, uint64_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_xsh_rr_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint64_t, uint128_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def setseq_xsh_rr_16_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint8_t, uint16_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_xsh_rr_32_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint16_t, uint32_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_xsh_rr_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint32_t, uint64_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_xsh_rr_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint64_t, uint128_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def mcg_xsh_rr_16_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint8_t, uint16_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def mcg_xsh_rr_32_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint16_t, uint32_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def mcg_xsh_rr_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint32_t, uint64_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def mcg_xsh_rr_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint64_t, uint128_t, pcg_detail.xsh_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv


# Predefined types for RXS M XS

def oneseq_rxs_m_xs_8_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint8_t, uint8_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_rxs_m_xs_16_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint16_t, uint16_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_rxs_m_xs_32_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint32_t, uint32_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_rxs_m_xs_64_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint64_t, uint64_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_rxs_m_xs_128_128(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint128_t, uint128_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def unique_rxs_m_xs_8_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint8_t, uint8_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_rxs_m_xs_16_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint16_t, uint16_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_rxs_m_xs_32_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint32_t, uint32_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_rxs_m_xs_64_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint64_t, uint64_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_rxs_m_xs_128_128(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint128_t, uint128_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def setseq_rxs_m_xs_8_8(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint8_t, uint8_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_rxs_m_xs_16_16(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint16_t, uint16_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_rxs_m_xs_32_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint32_t, uint32_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_rxs_m_xs_64_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint64_t, uint64_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_rxs_m_xs_128_128(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint128_t, uint128_t, pcg_detail.rxs_m_xs_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

# MCG versions don't make sense here, so aren't defined.


# Predefined types for XSL RR (only defined for "large" types)

def oneseq_xsl_rr_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint32_t, uint64_t, pcg_detail.xsl_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_xsl_rr_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint64_t, uint128_t, pcg_detail.xsl_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def unique_xsl_rr_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint32_t, uint64_t, pcg_detail.xsl_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_xsl_rr_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint64_t, uint128_t, pcg_detail.xsl_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def setseq_xsl_rr_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint32_t, uint64_t, pcg_detail.xsl_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_xsl_rr_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint64_t, uint128_t, pcg_detail.xsl_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def mcg_xsl_rr_64_32(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint32_t, uint64_t, pcg_detail.xsl_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def mcg_xsl_rr_128_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.mcg_base(uint64_t, uint128_t, pcg_detail.xsl_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv


# Predefined types for XSL RR RR (only defined for "large" types)

def oneseq_xsl_rr_rr_64_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint64_t, uint64_t, pcg_detail.xsl_rr_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def oneseq_xsl_rr_rr_128_128(*seed_args, **seed_kwargs):
    rv = pcg_detail.oneseq_base(uint128_t, uint128_t, pcg_detail.xsl_rr_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def unique_xsl_rr_rr_64_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint64_t, uint64_t, pcg_detail.xsl_rr_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def unique_xsl_rr_rr_128_128(*seed_args, **seed_kwargs):
    rv = pcg_detail.unique_base(uint128_t, uint128_t, pcg_detail.xsl_rr_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def setseq_xsl_rr_rr_64_64(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint64_t, uint64_t, pcg_detail.xsl_rr_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def setseq_xsl_rr_rr_128_128(*seed_args, **seed_kwargs):
    rv = pcg_detail.setseq_base(uint128_t, uint128_t, pcg_detail.xsl_rr_rr_mixin, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

# MCG versions don't make sense here, so aren't defined.


# Extended generators

def ext_std8(table_pow2, advance_pow2, BaseRNG, kdd=True, *seed_args, **seed_kwargs):
    rv = pcg_detail.Extended(table_pow2, advance_pow2, BaseRNG, oneseq_rxs_m_xs_8_8, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def ext_std16(table_pow2, advance_pow2, BaseRNG, kdd=True, *seed_args, **seed_kwargs):
    rv = pcg_detail.Extended(table_pow2, advance_pow2, BaseRNG, oneseq_rxs_m_xs_16_16, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def ext_std32(table_pow2, advance_pow2, BaseRNG, kdd=True, *seed_args, **seed_kwargs):
    rv = pcg_detail.Extended(table_pow2, advance_pow2, BaseRNG, oneseq_rxs_m_xs_32_32, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def ext_std64(table_pow2, advance_pow2, BaseRNG, kdd=True, *seed_args, **seed_kwargs):
    rv = pcg_detail.Extended(table_pow2, advance_pow2, BaseRNG, oneseq_rxs_m_xs_64_64, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv

def ext_oneseq_rxs_m_xs_32_32(table_pow2, advance_pow2, kdd=True, *seed_args, **seed_kwargs):
    rv = ext_std32(table_pow2, advance_pow2, oneseq_rxs_m_xs_32_32, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def ext_mcg_xsh_rs_64_32(table_pow2, advance_pow2, kdd=True, *seed_args, **seed_kwargs):
    rv = ext_std32(table_pow2, advance_pow2, mcg_xsh_rs_64_32, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def ext_oneseq_xsh_rs_64_32(table_pow2, advance_pow2, kdd=True, *seed_args, **seed_kwargs):
    rv = ext_std32(table_pow2, advance_pow2, oneseq_xsh_rs_64_32, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def ext_setseq_xsh_rr_64_32(table_pow2, advance_pow2, kdd=True, *seed_args, **seed_kwargs):
    rv = ext_std32(table_pow2, advance_pow2, setseq_xsh_rr_64_32, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def ext_mcg_xsl_rr_128_64(table_pow2, advance_pow2, kdd=True, *seed_args, **seed_kwargs):
    rv = ext_std64(table_pow2, advance_pow2, mcg_xsl_rr_128_64, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def ext_oneseq_xsl_rr_128_64(table_pow2, advance_pow2, kdd=True, *seed_args, **seed_kwargs):
    rv = ext_std64(table_pow2, advance_pow2, oneseq_xsl_rr_128_64, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
def ext_setseq_xsl_rr_128_64(table_pow2, advance_pow2, kdd=True, *seed_args, **seed_kwargs):
    rv = ext_std64(table_pow2, advance_pow2, setseq_xsl_rr_128_64, kdd, seed=False)
    rv.seed(*seed_args, **seed_kwargs)
    return rv
