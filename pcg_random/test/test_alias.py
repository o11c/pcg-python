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

import pcg_random

import types
import pytest


class TestAlias:
    @pytest.mark.parametrize('rng_name, rng_class', [
        (k, v)
        for mod in [pcg_random, pcg_random.pcg_engines]
        for k, v in sorted(vars(mod).items())
        if isinstance(v, types.FunctionType) and not k.startswith(('_', 'ext'))
        ])
    def test_alias(self, rng_name, rng_class):
        rng = rng_class(seed=False)
        assert rng_class.itype is rng.itype
        assert rng_class.xtype is rng.xtype
