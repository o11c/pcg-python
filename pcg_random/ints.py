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


# TODO once 3.6 becomes common, just use __init_subclass__
class _unsigned_int_meta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        if 'BITS' in cls.__dict__:
            cls.MOD = 1 << cls.BITS
            cls.MASK = cls.MOD - 1
            if not cls.BITS % 4:
                cls.NYBBLES = cls.BITS // 4
            if not cls.BITS % 8:
                cls.BYTES = cls.BITS // 8
        if hasattr(cls, 'BITS'):
            cls.MIN = cls.ZERO = cls(0)
            cls.ONE = cls(1)
            cls.MAX = cls(cls.MASK)
            cls.HIGH = cls(1 << (cls.BITS - 1))


class _unsigned_int_base(metaclass=_unsigned_int_meta):
    def __init__(self, value=0):
        value = self._unwrap(value)
        self._value = value & self.MASK

    def __repr__(self):
        cls = self.__class__
        cls_name = cls.__qualname__
        return '%s(%r)' % (cls_name, self._value)

    @staticmethod
    def _unwrap(value):
        if isinstance(value, _unsigned_int_base):
            return value._value
        else:
            assert type(value) is int
            return value

    @classmethod
    def coerce(cls, other):
        if isinstance(other, _unsigned_int_base):
            if cls is not type(other):
                raise TypeError
            return other
        else:
            assert type(other) is int
            if other < 0:
                other += cls.MOD
            if not 0 <= other <= cls.MAX:
                raise ValueError
            return cls._make(other)

    @classmethod
    def _coerce_value(cls, other):
        if isinstance(other, _unsigned_int_base):
            if cls is not type(other):
                raise TypeError
            return other._value
        else:
            assert type(other) is int
            if other < 0:
                other += cls.MOD
            if not 0 <= other <= cls.MAX:
                raise ValueError
            return other

    @classmethod
    def _make(cls, val):
        return cls(val)

    def __eq__(self, other):
        return self._value == self._unwrap(other)
    def __ne__(self, other):
        return self._value != self._unwrap(other)
    def __lt__(self, other):
        return self._value < self._unwrap(other)
    def __gt__(self, other):
        return self._value > self._unwrap(other)
    def __le__(self, other):
        return self._value <= self._unwrap(other)
    def __ge__(self, other):
        return self._value >= self._unwrap(other)

    def __add__(self, other):
        other = self._coerce_value(other)
        return self._make(self._value + other)
    __radd__ = __add__

    def __and__(self, other):
        other = self._coerce_value(other)
        return self._make(self._value & other)
    __rand__ = __and__

    def __bool__(self):
        return bool(self._value)

    def __int__(self):
        return self._value
    __index__ = __int__

    def __invert__(self):
        return self._make(~self._value)

    def __lshift__(self, other):
        assert type(other) is int
        assert 0 <= other < self.BITS
        return self._make(self._value << other)

    def __mul__(self, other):
        other = self._coerce_value(other)
        return self._make(self._value * other)
    __rmul__ = __mul__

    def __neg__(self):
        return self._make(-self._value)

    def __or__(self, other):
        other = self._coerce_value(other)
        return self._make(self._value | other)
    __ror__ = __or__

    def __rshift__(self, other):
        assert type(other) is int
        assert 0 <= other < self.BITS
        return self._make(self._value >> other)

    def __sub__(self, other):
        other = self._coerce_value(other)
        return self._make(self._value - other)
    def __rsub__(self, other):
        # This is the only asymmetrical operation,
        # since we don't need division or modulus.
        other = self._coerce_value(other)
        return self._make(other - self._value)

    def __xor__(self, other):
        other = self._coerce_value(other)
        return self._make(self._value ^ other)
    __rxor__ = __xor__

    def rotl(self, rot):
        BITS = self.BITS
        assert type(rot) is int
        assert 0 <= rot < BITS
        value = self._value
        MASK = BITS - 1
        return self._make(value << rot | value >> (-rot & MASK))

    def rotr(self, rot):
        BITS = self.BITS
        assert type(rot) is int
        assert 0 <= rot < self.BITS
        value = self._value
        MASK = BITS - 1
        return self._make(value >> rot | value << (-rot & MASK))

    @classmethod
    def urandom(cls):
        import os
        return cls._make(int.from_bytes(os.urandom(cls.BYTES), 'big'))


class uint8_t(_unsigned_int_base): BITS = 8
class uint16_t(_unsigned_int_base): BITS = 16
class uint32_t(_unsigned_int_base): BITS = 32
class uint64_t(_unsigned_int_base): BITS = 64
class uint128_t(_unsigned_int_base): BITS = 128
class uintptr_t(globals()['uint%d_t' % (__import__('sys').maxsize.bit_length() + 1)]): pass
