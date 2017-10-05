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

import abc


class Pointer(metaclass=abc.ABCMeta):
    ''' Horrible porting aid.

        Distressingly useful.
    '''
    def __repr__(self):
        return '<Pointer to %r>' % (self.get(),)
    @abc.abstractmethod
    def get(self):
        pass
    @abc.abstractmethod
    def set(self, value):
        pass

class ValuePointer(Pointer):
    def __init__(self, value):
        self._value = value
    def get(self):
        return self._value
    def set(self, value):
        self._value = value

class ItemPointer(Pointer):
    def __init__(self, container, key):
        self._container = container
        self._key = key
    def get(self):
        return self._container[self._key]
    def set(self, value):
        self._container[self._key] = value

class AttrPointer(Pointer):
    def __init__(self, obj, attr):
        self._obj = obj
        self._attr = attr
    def get(self):
        return getattr(self._obj, self._attr)
    def set(self, value):
        setattr(self._obj, self._attr, value)

del abc
