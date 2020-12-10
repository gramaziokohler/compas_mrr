"""
********************************************************************************
total_station_robot_localization.utils
********************************************************************************

.. currentmodule:: total_station_robot_localization.utils

.. autosummary::
    :toctree: generated/

    temp_change_compas_precision
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

try:
    from typing import List

    import Rhino.Geometry  # noqa: F401 # Import for type checking
except ImportError:
    pass


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


def rgtransform_to_matrix(rgM):
    # type: (Rhino.Geometry.Transform) -> List[List[float]]
    """Convert :class:`Rhino.Geometry.Transform` to transformation matrix.

    Parameters
    ----------
    rgM : :class:`Rhino.Geometry.Transform`

    Returns
    -------
    :class:`list` of :class:`list` of :class:`float`.
    """
    try:
        import Rhino
    except ImportError:
        raise RuntimeError("Can't import Rhino.")

    M = [[rgM.Item[i, j] for j in range(4)] for i in range(4)]
    return M
