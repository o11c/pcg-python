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

def maybe_vars(obj):
    return getattr(obj, '__dict__', {})

def mro_of(cls):
    # needed to get the MRO of `type` itself (and its subclasses,
    # i.e. other metaclasses).
    return type(cls).mro(cls)

Py_TPFLAGS_HEAPTYPE = (1 << 9)

def is_pure_python_type(cls):
    return bool(cls.__flags__ & Py_TPFLAGS_HEAPTYPE)

def smart_dir(obj):
    rv = set()
    if not isinstance(obj, type):
        rv.update(maybe_vars(obj))
    else:
        for cls in mro_of(obj):
            if is_pure_python_type(cls):
                rv.update(maybe_vars(cls))
    ty = type(obj)
    for cls in mro_of(ty):
        if is_pure_python_type(cls):
            rv.update(maybe_vars(cls))
    rv.difference_update(('__dict__', '__doc__', '__module__', '__weakref__'))
    return rv

dynamic_mixin_blacklist = {
        '__init__',
        '__new__',
        '__slots__',
}

def dynamic_mixin(self, *mixins, protected=False):
    ''' Used to simulate C++ inheritance from a template argument.
    '''
    assert not isinstance(self, type)
    self_vars = smart_dir(self)

    for mixin in mixins:
        assert isinstance(mixin, type)
        for k in sorted(smart_dir(mixin)):
            if k in dynamic_mixin_blacklist:
                raise KeyError('Blacklisted key: %r' % k)
            v = getattr(mixin, k)
            k = '_' + k if protected and not k.startswith('_') else k
            if k in self_vars:
                ov = getattr(self, k)
                raise KeyError('Duplicate key: %r, old value: %r, new value: %r)' % (k, ov, v))
            get = getattr(v, '__get__', None)
            if get is not None:
                v = get(self)
            setattr(self, k, v)
            self_vars.add(k)
