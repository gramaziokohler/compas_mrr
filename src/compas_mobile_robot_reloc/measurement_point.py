from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas.geometry

from compas_mobile_robot_reloc import utils
from compas_mobile_robot_reloc.utils import TYPE_CHECKING
from compas_mobile_robot_reloc.utils import cgpoint_to_rgpoint

if TYPE_CHECKING:
    from typing import Tuple
    from typing import Union


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


# Make MeasurementPoint available from utils for backwards compatibility
# with compas_mobile_robot_reloc <= v1.0.4
utils.MeasurementPoint = MeasurementPoint  # type: ignore[attr-defined]
