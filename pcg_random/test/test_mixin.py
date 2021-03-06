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

from pcg_random.mixin import dynamic_mixin, smart_dir

import pytest


class TestDynamicMixin:
    def test_okay(self):
        class Foo:
            def x(self, *args):
                return args
        class Mixin1:
            def y(self, *args):
                return args
        class Mixin2:
            def z(self, *args):
                return args
        foo = Foo()

        dynamic_mixin(foo, Mixin1, Mixin2)
        assert foo.x() == ()
        assert foo.x(1, 2, 3) == (1, 2, 3)
        assert foo.y() == ()
        assert foo.y(1, 2, 3) == (1, 2, 3)
        assert foo.z() == ()
        assert foo.z(1, 2, 3) == (1, 2, 3)

    def test_collision(self):
        class Foo:
            x = 1
        class Mixin1:
            x = 2
        class Mixin2a:
            def y(self):
                pass
        class Mixin2b:
            def y(self):
                pass

        foo = Foo()
        with pytest.raises(KeyError):
            dynamic_mixin(foo, Mixin1)

        foo = Foo()
        with pytest.raises(KeyError):
            dynamic_mixin(foo, Mixin2a, Mixin2b)

    def test_inherit(self):
        class Foo:
            x = 1
        class Bar(Foo):
            pass
        class MixinBase:
            x = 2
        class Mixin(MixinBase):
            pass
        bar = Bar()

        with pytest.raises(KeyError):
            dynamic_mixin(bar, Mixin)
        #TODO: is there a way to make this work sanely?
        #assert bar.x == 2
        assert bar.x == 1

    def test_blacklist(self):
        class Foo:
            pass
        class Mixin1:
            def __init__(self):
                pass
        class Mixin2:
            def __new__(cls):
                pass
        class Mixin3:
            __slots__ = ()

        foo = Foo()
        with pytest.raises(KeyError):
            dynamic_mixin(foo, Mixin1)

        foo = Foo()
        with pytest.raises(KeyError):
            dynamic_mixin(foo, Mixin2)

        foo = Foo()
        with pytest.raises(KeyError):
            dynamic_mixin(foo, Mixin3)

    def test_property(self):
        class Foo:
            x = 1
            def __init__(self):
                self.y = 2
        class Mixin:
            @property
            def px(self):
                return self.x
            @property
            def py(self):
                return self.y
        foo = Foo()
        dynamic_mixin(foo, Mixin)
        foo.x = 3
        foo.y = 4
        assert foo.px == 1
        assert foo.py == 2

    def test_protected(self):
        class Foo:
            x = 1
            _y = 2
        class Mixin1:
            x = 3
        class Mixin2:
            y = 4
        class Mixin3:
            z = 5
            _z = 6

        foo = Foo()
        dynamic_mixin(foo, Mixin1, protected=True)
        assert foo._x == 3

        foo = Foo()
        with pytest.raises(KeyError):
            dynamic_mixin(foo, Mixin2, protected=True)

        foo = Foo()
        with pytest.raises(KeyError):
            dynamic_mixin(foo, Mixin3, protected=True)


class TestSmartDir:
    def test_meta(self):
        class FooMetaMeta(type):
            x = 1
        class FooMeta(type, metaclass=FooMetaMeta):
            y = 2
        class Foo(metaclass=FooMeta):
            z = 3
        foo = Foo()
        foo.w = 4

        assert getattr(Foo, 'x', None) is None
        assert getattr(Foo, 'y', None) == 2
        assert getattr(Foo, 'z', None) == 3
        assert getattr(Foo, 'w', None) is None
        assert smart_dir(Foo) == {'y', 'z'}

        assert getattr(foo, 'x', None) is None
        assert getattr(foo, 'y', None) is None
        assert getattr(foo, 'z', None) == 3
        assert getattr(foo, 'w', None) == 4
        assert smart_dir(foo) == {'z', 'w'}

    def test_slots(self):
        class Foo:
            __slots__ = ('a', 'b')
        foo = Foo()

        assert smart_dir(Foo) == {'__slots__', 'a', 'b'}
        assert smart_dir(foo) == {'__slots__', 'a', 'b'}
