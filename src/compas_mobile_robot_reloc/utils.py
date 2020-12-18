"""
********************************************************************************
Utilities
********************************************************************************
"""
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
        raise Exception("Can't import Rhino in current environment.")


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
    from typing import Tuple
    from typing import Union


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


class MeasurementPoint(compas.geometry.Point):
    """A :class:`compas.geometry.Point` with some CSV pointlist related methods."""

    def __init__(
        self,
        x,  # type: float
        y,  # type: float
        z,  # type: float
        pt_name,  # type: str
        attrs=None,  # type: Union[None, dict]
    ):  # type: (...) -> None
        super(MeasurementPoint, self).__init__(x, y, z)
        self.pt_name = pt_name
        self.attrs = attrs or {}

    def __repr__(self):  # type: () -> str
        return "Point ID: {}, Location: {}, {}, {}".format(
            self.pt_name, self.x, self.y, self.z
        )

    @property
    def prefix(self):  # type: () -> str
        """Point prefix from data source."""
        return self._split_pt_name()[0]

    @property
    def idx(self):  # type: () -> int
        """Point index from data source."""
        return self._split_pt_name()[1]

    def as_rgpoint(self):  # type: () -> compas.geometry.Point
        """Get a point representation in Rhino."""
        return cgpoint_to_rgpoint(self)

    def _split_pt_name(self):  # type: () -> Tuple[str, int]
        idx = ""

        for n, elem in enumerate(self.pt_name[::-1]):
            if elem.isdigit():
                idx = elem + idx  # add to front of str
            else:
                idx_last_char_idx = len(self.pt_name) - n
                break

        prefix = self.pt_name[:idx_last_char_idx]

        try:
            _idx = int(idx)
        except ValueError:
            _idx = 0

        return prefix, _idx
