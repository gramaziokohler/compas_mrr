"""Utilities"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas.geometry

try:
    import Rhino.Geometry
except ImportError:
    pass


def _ensure_rhino():  # type: () -> None
    if not compas.RHINO:
        raise ImportError("Can't import Rhino in current environment.")


def _is_type_checking():  # type: () -> bool
    try:
        import typing  # noqa: F401

        if typing.TYPE_CHECKING:
            return True

    except ImportError:
        pass

    return False


TYPE_CHECKING = _is_type_checking()  # type: bool

if TYPE_CHECKING:
    from typing import List


def rgpoint_to_cgpoint(pt):
    # type: (Rhino.Geometry.Point3d) -> compas.geometry.Point
    """Convert :class:`Rhino.Geometry.Point3d` to :class:`compas.geometry.Point`.

    Parameters
    ----------
    pt
        Plane object to convert

    Returns
    -------
        Resulting point object
    """
    return compas.geometry.Point(pt.X, pt.Y, pt.Z)


def cgpoint_to_rgpoint(pt):
    # type: (compas.geometry.Point) -> (Rhino.Geometry.Point3d)
    """Convert :class:`compas.geometry.Point` to :class:`Rhino.Geometry.Point`."""
    return Rhino.Geometry.Point3d(*list(pt))


def cgframe_to_rgplane(frame):  # type: (compas.geometry.Frame) -> Rhino.Geometry.Plane
    """Convert :class:`compas.Geometry.Frame` to :class:`Rhino.Geometry.Plane`."""  # noqa: E501
    origin = Rhino.Geometry.Point3d(*list(frame.point))
    x_vec = Rhino.Geometry.Vector3d(*list(frame.xaxis))
    y_vec = Rhino.Geometry.Vector3d(*list(frame.yaxis))

    return Rhino.Geometry.Plane(origin, x_vec, y_vec)


def rgtransform_to_cgtransformation(rgT):
    # type: (Rhino.Geometry.Transform) -> compas.geometry.Transformation
    """Convert :class:`Rhino.Geometry.Transform` to :class:`compas.geometry.Transformation`."""  # noqa: E501
    M = rgtransform_to_matrix(rgT)
    return compas.geometry.Transformation.from_matrix(M)


def rgtransform_to_matrix(rgT):  # type: (Rhino.Geometry.Transform) -> List[List[float]]
    """Convert :class:`Rhino.Geometry.Transform` to transformation matrix."""
    return [[rgT.Item[i, j] for j in range(4)] for i in range(4)]


def cgtransformation_to_rgtransform(cgT):
    # type: (compas.geometry.Transformation) -> Rhino.Geometry.Transform
    """Convert :class:`compas.geometry.Transformation` to :class:`Rhino.Geometry.Transform`."""  # noqa: E501
    _ensure_rhino()

    M = cgT.matrix

    return matrix_to_rgtransform(M)


def matrix_to_rgtransform(M):  # type: (List[List[float]]) -> Rhino.Geometry.Transform
    """Create :class:`Rhino.Geometry.Transform` from a transformation matrix."""
    _ensure_rhino()

    rgT = Rhino.Geometry.Transform()

    for i, row in enumerate(M):
        for j, val in enumerate(row):
            rgT[i, j] = val

    return rgT
