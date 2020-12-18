from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Transformation
from numpy import array
from pytest import approx
from pytest import fixture

from compas_mobile_robot_reloc.xforms import _coerce_cg_xform
from compas_mobile_robot_reloc.xforms import worldxy_to_robot_base_xform
from compas_mobile_robot_reloc.xforms import xform_to_xyz_quaternion


@fixture
def rcf():
    return Frame([100, 100, 100], [1, 0, 0], [0, 0, 1])


@fixture
def rcf_matrix():
    return [
        [1.0, 0.0, 0.0, -100],
        [0.0, 0.0, 1.0, -100],
        [0.0, -1.0, 0.0, 100],
        [0.0, 0.0, 0.0, 1.0],
    ]


@fixture
def rcf_xform(rcf_matrix):
    return Transformation.from_matrix(rcf_matrix)


def test__coerce_cg_xform_cg_xform():
    T = Transformation()

    assert T == _coerce_cg_xform(T)


def test__coerce_cg_xform_ndarray(rcf_matrix):
    _array = array(rcf_matrix)

    assert isinstance(_coerce_cg_xform(_array), Transformation)


def test_worldxy_to_robot_base_xform(rcf, rcf_xform):
    print(Transformation.from_frame(rcf))
    assert worldxy_to_robot_base_xform(rcf) == rcf_xform


def test_xform_to_xyz_quaternion(rcf_matrix):
    assert xform_to_xyz_quaternion(rcf_matrix) == approx(
        [-100, -100, 100, 0.707, -0.707, 0, 0], abs=1e-03
    )
