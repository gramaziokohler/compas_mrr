from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Transformation
from pytest import fixture
from pytest import raises

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
def rcf_xform():
    # def rcf_xform(rcf_matrix):
    M = [
        [1.0, 0.0, 0.0, -100],
        [0.0, 0.0, 1.0, -100],
        [0.0, -1.0, 0.0, 100],
        [0.0, 0.0, 0.0, 1.0],
    ]
    return Transformation.from_matrix(M)


@fixture
def rcf_xyz_quaternion():
    return [-100, -100, 100, 0.707, -0.707, 0, 0]


def test__coerce_cg_xform_cg_xform():
    T = Transformation()

    assert T == _coerce_cg_xform(T)


def test__coerce_cg_xform_ndarray(rcf_matrix):
    try:
        import numpy as np

        _array = np.array(rcf_matrix)

        assert isinstance(_coerce_cg_xform(_array), Transformation)

    except ImportError:
        pass


def test__coerce_cg_xform_none():
    with raises(TypeError):
        _coerce_cg_xform(None)


def test__coerce_cg_xform_invalid_sequence():
    with raises(TypeError):
        _coerce_cg_xform([None])


def test_worldxy_to_robot_base_xform(rcf, rcf_xform):
    assert worldxy_to_robot_base_xform(rcf) == rcf_xform


def test_xform_to_xyz_quaternion(rcf_matrix, rcf_xyz_quaternion):
    computed_quaternion = xform_to_xyz_quaternion(rcf_matrix)

    try:
        from pytest import approx

        assert approx(computed_quaternion, abs=1e-3) == rcf_xyz_quaternion

    except ImportError:  # IPY
        rounded_actual_result = [round(v, 3) for v in computed_quaternion]
        assert rounded_actual_result == rcf_xyz_quaternion
