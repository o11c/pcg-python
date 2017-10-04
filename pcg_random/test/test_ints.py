from pcg_random.ints import *

import pytest


def eq(a, b):
    # because they use value-only equality
    return type(a) == type(b) and a == b


class TestInts:
    def _test_common(self, u):
        def x(v):
            # identity function, for symmetry
            # x was chosen for being as visually distinct as possible
            return v

        assert eq(u(-1), u(u.MASK))
        assert eq(u(0), u(u.MOD))
        assert eq(u.MAX * u.MAX, u.ONE)
        assert 0 == u(0) == 0
        assert -1 != u(-1) != -1
        assert 0 < u(1) < 2
        assert 2 > u(1) > 0
        assert 0 <= u(1) <= 2
        assert 0 <= u(0) <= 0
        assert 2 >= u(1) >= 0
        assert 0 >= u(0) >= 0
        assert eq(u(6) + u(3), u(9))
        assert eq(x(6) + u(3), u(9))
        assert eq(u(6) + x(3), u(9))
        assert eq(u(6) & u(3), u(2))
        assert eq(x(6) & u(3), u(2))
        assert eq(u(6) & x(3), u(2))
        assert not u.ZERO
        assert u.ONE and u.MAX
        assert eq(int(u.ZERO), 0)
        assert eq(~u(0), u.MAX)
        assert eq(~u(1), u.MAX-1)
        assert eq(~u(2), u.MAX-2)
        assert eq(~u(3), u.MAX-3)
        assert eq(u.HIGH << 1, u.ZERO)
        assert eq(u(1) << 1, u(2))
        assert eq(u(6) * u(3), u(18))
        assert eq(x(6) * u(3), u(18))
        assert eq(u(6) * x(3), u(18))
        assert eq(-u(0), u.MAX + 1)
        assert eq(-u(1), u.MAX-0)
        assert eq(-u(2), u.MAX-1)
        assert eq(-u(3), u.MAX-2)
        assert eq(u(6) | u(3), u(7))
        assert eq(x(6) | u(3), u(7))
        assert eq(u(6) | x(3), u(7))
        assert eq(u(1) >> 1, u(0))
        assert eq(u(2) >> 1, u(1))
        assert eq(u(6) - u(2), u(4))
        assert eq(x(6) - u(2), u(4))
        assert eq(u(6) - x(2), u(4))
        assert eq(u(6) ^ u(3), u(5))
        assert eq(x(6) ^ u(3), u(5))
        assert eq(u(6) ^ x(3), u(5))
        assert eq(u(5).rotl(u.BITS - 1), u.HIGH | 2)
        assert eq(u(5).rotl(u.BITS - 2), u.HIGH >> 1 | 1)
        assert eq(u(5).rotl(u.BITS - 3), u.HIGH >> 2 | u.HIGH)
        assert eq(u(5).rotl(1), u(10))
        assert eq(u(5).rotl(2), u(20))
        assert eq(u(5).rotl(3), u(40))
        assert eq(u(5).rotr(1), u.HIGH | 2)
        assert eq(u(5).rotr(2), u.HIGH >> 1 | 1)
        assert eq(u(5).rotr(3), u.HIGH >> 2 | u.HIGH)
        assert eq(u(5).rotr(u.BITS - 1), u(10))
        assert eq(u(5).rotr(u.BITS - 2), u(20))
        assert eq(u(5).rotr(u.BITS - 3), u(40))
        for i in range(u.BITS):
            assert eq(u(5).rotl(i).rotr(i), u(5))
            assert eq(u(5).rotr(i).rotl(i), u(5))

    def test_u8(self, u=uint8_t):
        assert u.BITS == 8
        assert u.BYTES == 1
        assert u.MASK == 0xff
        assert u.MOD == 0x100
        assert u.HIGH == 0x80
        self._test_common(u)

    def test_u16(self, u=uint16_t):
        assert u.BITS == 16
        assert u.BYTES == 2
        assert u.MASK == 0xffff
        assert u.MOD == 0x10000
        assert u.HIGH == 0x8000
        self._test_common(u)

    def test_u32(self, u=uint32_t):
        assert u.BITS == 32
        assert u.BYTES == 4
        assert u.MASK == 0xffffffff
        assert u.MOD == 0x100000000
        assert u.HIGH == 0x80000000
        self._test_common(u)

    def test_u64(self, u=uint64_t):
        assert u.BITS == 64
        assert u.BYTES == 8
        assert u.MASK == 0xffffffffffffffff
        assert u.MOD == 0x10000000000000000
        assert u.HIGH == 0x8000000000000000
        self._test_common(u)

    def test_u128(self, u=uint128_t):
        assert u.BITS == 128
        assert u.BYTES == 16
        assert u.MASK == 0xffffffffffffffffffffffffffffffff
        assert u.MOD == 0x100000000000000000000000000000000
        assert u.HIGH == 0x80000000000000000000000000000000
        self._test_common(u)

    def test_uptr(self, u=uintptr_t):
        # Simply reuse the existing test function with a different class
        getattr(self, 'test_u%d' % u.BITS)(u)
