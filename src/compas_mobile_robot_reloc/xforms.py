"""Transformations"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg

from compas_mobile_robot_reloc.utils import TYPE_CHECKING

try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence

if TYPE_CHECKING:
    from typing import Any
    from typing import List


def _coerce_cg_xform(xform):  # type: (Any) -> cg.Transformation
    try:
        from Rhino.Geometry import Transform

        if isinstance(xform, Transform):
            from compas_mobile_robot_reloc.utils import rgtransform_to_matrix

            M = rgtransform_to_matrix(xform)
            return cg.Transformation.from_matrix(M)
    except ImportError:
        pass

    try:
        from numpy import ndarray

        if isinstance(xform, ndarray):
            M = xform.tolist()
            return cg.Transformation.from_matrix(M)
    except ImportError:
        pass

    if isinstance(xform, cg.Transformation):
        return xform

    if isinstance(xform, Sequence):
        try:
            T = cg.Transformation.from_matrix(xform)
            T.decomposed()  # raises type error on invalid T
            return T
        except TypeError:
            pass

    raise TypeError(
        "Can't convert {} to compas.geometry.Transformation".format(type(xform))
    )


def worldxy_to_robot_base_xform(robot_base_frame):
    # type: (cg.Frame) -> cg.Transformation
    """Get transformation from WCS origin to RCS origin.

    Parameters
    ----------
    robot_base_frame
        Robot base frame in WCS. The frame origin is the location of the RCS origo
        in WCS, the X axis and Y axis are the X and Y axes of the RCS in WCS.
    """
    frame_from = cg.Frame.worldXY()
    frame_to = robot_base_frame

    return cg.Transformation.from_change_of_basis(frame_from, frame_to)


def xform_to_xyz_quaternion(xform):  # type: (Any) -> List[float]
    """Convert transformation to :obj:`list` of coords and quaternion values.

    Parameters
    ----------
    xform
        Transformation to be converted. Can be given as
        :class:`Rhino.Geometry.Transform`,
        :class:`compas.geometry.Transformation`,
        :class:`numpy.ndarray`, or :obj:`list` of :obj:`list` of :obj:`float`.

    Returns
    -------
        X, Y, Z, QW, QX, QY, QZ values as a list.

    >>> from compas.geometry import Frame, Rotation, Translation
    >>> Tr = Translation.from_vector([100, 100, 100])
    >>> R = Rotation.from_frame(Frame.worldYZ())
    >>> T = Tr * R
    >>> xform_to_xyz_quaternion(T)
    [100.0, 100.0, 100.0, 0.5, 0.5, 0.5, 0.5]
    """
    xform = _coerce_cg_xform(xform)

    xyz = list(xform.translation_vector)

    wxyz = cg.Quaternion.from_rotation(xform.rotation).wxyz

    return xyz + wxyz
