from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from pytest import fixture

from compas_mobile_robot_reloc import three_pts_localization
from compas_mobile_robot_reloc.three_pts_localization import _coerce_frame
from compas_mobile_robot_reloc.three_pts_localization import _pts_to_frame


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
def example_pt_rcs():
    return Point(1000, 1250, 1500)


@fixture
def example_pt_wcs():
    return Point(21910.426861, 15663.519267, -2714.911982)


@fixture
def orthogonal_frame(rcs_coords):
    pt = rcs_coords[0]
    return Frame(pt, Point(1, 0, 0), Vector(0, 1, 0))


def test__pts_to_frame(rcs_coords, orthogonal_frame):
    assert _pts_to_frame(rcs_coords) == orthogonal_frame


def test__coerce_frame(rcs_coords, orthogonal_frame):
    assert _coerce_frame(rcs_coords) == orthogonal_frame
    assert _coerce_frame(orthogonal_frame) == orthogonal_frame


def test_three_pts_localization(rcs_coords, wcs_coords, example_pt_rcs, example_pt_wcs):
    robot_base_wcs = three_pts_localization(rcs_coords, wcs_coords)

    transformed_pt = robot_base_wcs.to_local_coordinates(example_pt_rcs)

    try:
        from pytest import approx

        assert list(transformed_pt) == approx(list(example_pt_wcs))
    except ImportError:
        rounded_transformed_pt = [round(c, 2) for c in list(transformed_pt)]
        rounded_example_pt = [round(c, 2) for c in list(example_pt_wcs)]
        assert rounded_transformed_pt == rounded_example_pt
