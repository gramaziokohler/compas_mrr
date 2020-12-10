"""Transformation functions for localization using compas."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import quaternion_from_matrix
from compas.geometry import translation_from_matrix

from total_station_robot_localization.utils import temp_change_compas_precision

try:
    import typing
except ImportError:
    pass
else:
    if typing.TYPE_CHECKING:
        from typing import List
        from typing import Any


@temp_change_compas_precision("12f")
def worldxy_to_robot_base_xform(robot_base_frame):  # type: (Frame) -> Transformation
    """Calculate the transformation matrix for transformations between WCS to RCS.

    Parameters
    ----------
    robot_base_frame
        Robot base frame in WCS. The frame origin is the location of the RCS origo
        in WCS, the X axis and Y axis are the X and Y axes of the RCS in WCS.

    Returns
    -------
        The transformation matrix.
    """
    return Transformation.change_basis(Frame.worldXY(), robot_base_frame)


@temp_change_compas_precision("12f")
def xform_to_xyz_quaternion(xform):  # type: (Any) -> List[float]
    """Convert transformation to :obj:`list` of coords and quaternion values.

    Parameters
    ----------
    xform
        Transformation to be converted. Can be given as
        :class:`Rhino.Geometry.Transform`, :class:`compas.geometry.Transformation`
        or :obj:`list` of :obj:`list` of :obj:`float`.

    Returns
    -------
        X, Y, Z, QW, QX, QY, QZ values as a list.

    >>> from compas.geometry import Frame, Rotation, Translation
    >>> Tr = Translation([100, 100, 100])
    >>> R = Rotation.from_frame(Frame.worldYZ())
    >>> T = Tr * R
    >>> xform_to_xyz_quaternion(T)
    [100.0, 100.0, 100.0, 0.5, 0.5, 0.5, 0.5]
    """
    M = _get_matrix(xform)
    xyzwxyz = _matrix_to_xyz_quaternion(M)

    return xyzwxyz


def _get_matrix(xform):  # type: (Any) -> List[List[float]]

    try:
        from Rhino.Geometry import Transform

        from total_station_robot_localization.utils import rgtransform_to_matrix
    except ImportError:
        pass
    else:
        if isinstance(xform, Transform):
            return rgtransform_to_matrix(xform)

    try:
        from numpy import ndarray
    except ImportError:
        pass
    else:
        if isinstance(xform, ndarray):
            return xform.tolist()  # type: ignore

    if isinstance(xform, Transformation):
        return xform.matrix  # type: ignore

    return xform  # type: ignore


def _matrix_to_xyz_quaternion(M):  # type: (List[List[float]]) -> List[float]
    xyz = translation_from_matrix(M)
    quaternion = quaternion_from_matrix(M)

    return xyz + quaternion  # type: ignore
