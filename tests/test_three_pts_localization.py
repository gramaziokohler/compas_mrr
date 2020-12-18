from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Point
from pytest import approx
from pytest import fixture

from compas_mobile_robot_reloc import three_pts_localization


@fixture
def rcs_coords():
    coords = [[1000, 1000, 500], [2000, 1000, 500], [1000, 2000, 500]]

    return [Point(*c) for c in coords]


@fixture
def wcs_coords():
    coords = [
        [9759.510383, 25270.12503, 4484.114176],
        [8939.012559, 24698.481189, 4486.691114],
        [10331.140105, 24449.701785, 4496.16237],
    ]

    return [Point(*c) for c in coords]


@fixture
def arbitrary_pt_rcs():
    return Point(1000, 1250, 1500)


@fixture
def arbitrary_pt_wcs():
    return Point(21910.426861, 15663.519267, -2714.911982)


def test_three_pts_localization(
    rcs_coords, wcs_coords, arbitrary_pt_rcs, arbitrary_pt_wcs
):
    robot_base_wcs = three_pts_localization(rcs_coords, wcs_coords)

    computed_arbitrary_pt_wcs = robot_base_wcs.to_local_coordinates(arbitrary_pt_rcs)

    assert list(computed_arbitrary_pt_wcs) == approx(list(arbitrary_pt_wcs))
