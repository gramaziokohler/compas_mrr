"""Three points method for robot relocalization.

Code adapted from source code by Selen Ercan and Sandro Meier at Gramazio
Kohler Research, ETH Zurich (2019).

Original code:
https://github.com/gramaziokohler/IF_jamming/blob/master/if_jamming/localization/transform.py

Ercan, Selen, Sandro Meier, Fabio Gramazio, and Matthias Kohler. 2019.
"Automated Localization of a Mobile Construction Robot with an External
Measurement Device." In Proceedings of the 36th International Symposium on
Automation and Robotics in Construction (ISARC 2019), 929-36. International
Association on Automation and Robotics in Construction.
https://doi.org/10.3929/ethz-b-000328442.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Transformation

from compas_mobile_robot_reloc.utils import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from typing import Union

    from compas.geometry import Point


def _pts_to_frame(pts):  # type: (Point) -> Frame
    return Frame.from_points(*pts)


def _coerce_frame(frame_or_pts):  # type: (Union[List[Point], Frame]) -> Frame
    if isinstance(frame_or_pts, Frame):
        return frame_or_pts

    return _pts_to_frame(frame_or_pts)


__all__ = ["three_pts_localization"]


def three_pts_localization(
    rcs_coords, wcs_coords
):  # type: (List[Point], List[Point]) -> Frame
    """Get the robot base frame in WCS using three points method.

    Parameters
    ----------
    rcs_coords
        List of the RCS coordinates used for measurements.
    wcs_coords
        List of the WCS coordinates used for measurements.

    Returns
    -------
        The base frame of the robot in WCS.
    """
    recorded_frame_rcs = _coerce_frame(rcs_coords)
    recorded_frame_wcs = _coerce_frame(wcs_coords)

    T = Transformation.from_frame_to_frame(recorded_frame_rcs, recorded_frame_wcs)

    wcs_robot_base = Frame.worldXY()
    wcs_robot_base.transform(T)

    return wcs_robot_base
