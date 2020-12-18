from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg
import pytest
from compas.rpc import Proxy


@pytest.fixture
def wcs_pts():
    coords = [
        [15402.885, 24560.608, 1046.399],
        [15117.993, 23725.867, 1208.917],
        [15223.168, 22797.331, 2399.654],
        [16199.274, 22003.423, 1362.059],
        [16786.777, 23083.323, 3974.498],
        [17965.302, 23314.847, 4033.842],
        [18982.944, 24283.387, 3544.996],
        [18539.657, 25105.912, 2822.457],
        [17748.109, 25368.456, 2296.253],
    ]
    return [cg.Point(*c) for c in coords]


@pytest.fixture
def rcs_pts():

    coords = [
        [-2306.777, -271.836, -108.456],
        [-2306.726, -1153.883, 53.651],
        [-1908.872, -2001.106, 1251.384],
        [-734.537, -2442.080, 201.813],
        [-514.716, -1236.923, 2818.192],
        [520.430, -645.945, 2879.326],
        [1171.776, 591.959, 2397.131],
        [499.173, 1232.814, 1660.649],
        [-333.942, 1232.847, 1134.185],
    ]
    return [cg.Point(*c) for c in coords]


def test_proxy(wcs_pts, rcs_pts):
    with Proxy(
        "compas_mobile_robot_reloc.arbitrary_pts_localization", python="python"
    ) as proxy:
        result = proxy.arbitrary_pts_localization(rcs_pts, wcs_pts)
        print(type(result))
        print(cg.Frame(*result))
