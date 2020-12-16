"""
********************************************************************************
compas_mobile_robot_reloc.utils
********************************************************************************

.. currentmodule:: compas_mobile_robot_reloc.utils

.. autosummary::
    :toctree: generated/
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas.geometry as cg

try:
    from typing import List
except ImportError:
    pass

try:
    import Rhino.Geometry as rg
except ImportError:
    pass


def _ensure_rhino():  # type: () -> None
    try:
        import Rhino  # noqa: F401
    except ImportError:
        raise Exception("Can't import Rhino in current environment.")


def temp_change_compas_precision(precision):
    """Decorate function to run with specified compas.PRECISION."""

    def decorator(func):
        def wrapped_func(*args, **kwargs):
            prev_precision = compas.PRECISION
            compas.PRECISION = precision

            result = func(*args, **kwargs)

            compas.PRECISION = prev_precision
            return result

        return wrapped_func

    return decorator


def rgpoint_to_cgpoint(pt):
    # type: (rg.Point3d) -> compas.geometry.Point
    """Convert :class:`Rhino.Geometry.Point3d` to :class:`compas.geometry.Point`.

    Parameters
    ----------
    pt
        Plane object to convert

    Returns
    -------
        Resulting point object
    """
    return cg.Point(pt.X, pt.Y, pt.Z)


def rgtransform_to_cgtransformation(rgT):
    # type: (rg.Transform) -> cg.Transformation
    """Convert :class:`Rhino.Geometry.Transform` to :class:`compas.geometry.Transformation`."""  # noqa: E501
    _ensure_rhino()

    M = rgtransform_to_matrix(rgT)
    return cg.Transformation.from_matrix(M)


def rgtransform_to_matrix(rgT):  # type: (rg.Transform) -> List[List[float]]
    """Convert :class:`Rhino.Geometry.Transform` to transformation matrix."""
    return [[rgT.Item[i, j] for j in range(4)] for i in range(4)]


def cgtransformation_to_rgtransform(cgT):
    # type: (compas.geometry.Transformation) -> rg.Transform
    """Convert :class:`compas.geometry.Transformation` to :class:`Rhino.Geometry.Transform`."""  # noqa: E501
    _ensure_rhino()

    M = cgT.matrix

    return matrix_to_rgtransform(M)


def matrix_to_rgtransform(M):  # type: (List[List[float]]) -> rg.Transform
    """Create :class:`Rhino.Geometry.Transform` from a transformation matrix."""
    _ensure_rhino()
    rgT = rg.Transform()

    for i, row in enumerate(M):
        for j, val in enumerate(row):
            rgT[i, j] = val

    return rgT
