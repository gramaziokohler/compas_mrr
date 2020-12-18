"""
*******************************************************************************
Arbitrary points method for robot relocalization.
*******************************************************************************
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import tempfile
from functools import reduce

import numpy as np
from scipy.optimize import minimize

from compas_mobile_robot_reloc.utils import TYPE_CHECKING

try:
    from pathlib import Path
except ImportError:
    if sys.version_info.major < 3:
        raise Exception("Python 3 is required to run this module.")
    else:
        raise

if TYPE_CHECKING:
    from typing import List

    from scipy.optimize import OptimizeResult


def _objective_function(
    x,  # type: List[float]
    rcs_coords,  # type: List[List[float]]
    wcs_coords,  # type: List[List[float]]
):  # type: (...) -> float
    """Objective function for the optimization problem.

    Parameters
    ----------
    x
        The optimization variable (9x1)
    args : :obj:`tuple`
        The localization points and the measurements as a tuple of two
        dimensional arrays where each row is one point. The columns are the X,
        Y and Z coordinates.

    Returns
    -------
    :obj:`float`
        The cost for the given optimization variable values.
    """
    origin = np.array(x[0:3])
    x_vec = np.array(x[3:6])
    y_vec = np.array(x[6:9])
    z_vec = np.cross(x_vec, y_vec)

    cost = 0
    for point, measurement in zip(rcs_coords, wcs_coords):
        # Calculate the deviation from the measurement using the given
        # coordinate system (optimization variable) and add the square of it to
        # the cost.
        deviation = np.power(
            origin
            + point[0] * x_vec
            + point[1] * y_vec
            + point[2] * z_vec
            - measurement,
            2,
        )
        cost += sum(deviation)

    return cost


def _nonlinear_constraints(x):  # type: (List[float]) -> List[float]
    """Constraints for the optimization problem.

    Parameters
    ----------
    x
        The optimization variable (9x1).

    Returns
    -------
    :obj:`list` of :obj:`float`
        An array that contains the values when the constraints are evaluated at
        `x`.
    """
    return [
        # x and y need to be orthogonal (i.e. scalar product = 0)
        x[3] * x[6] + x[4] * x[7] + x[5] * x[8],
        x[3] ** 2 + x[4] ** 2 + x[5] ** 2 - 1,  # |x| = 1
        x[6] ** 2 + x[7] ** 2 + x[8] ** 2 - 1,  # |y| = 1
    ]


def _nonlinear_jacobian(x):  # type: (List[float]) -> List[List[float]]
    """Jacobian for the constraints.

    Parameters
    ----------
    x
        The optimization variable (9x1).

    Returns
    -------
        The jacobian of the nonlinear constraints.
    """
    return [
        [0, 0, 0, x[6], x[7], x[8], x[3], x[4], x[5]],
        [0, 0, 0, 2 * x[3], 2 * x[4], 2 * x[5], 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2 * x[6], 2 * x[7], 2 * x[8]],
    ]


def _plot(
    rcs_coords,  # type: List[List[float]]
    wcs_coords,  # type: List[List[float]]
    results,  # type: OptimizeResult
):  # type: (...) -> None
    """Create plots to visualize multiple consecutive results from a solver."""
    import matplotlib.pyplot as plt

    rcs_coords = np.array(rcs_coords)
    wcs_coords = np.array(wcs_coords)

    plot_dir = Path(tempfile.mkdtemp(prefix="localization_"))
    print("Saving plots to {}".format(plot_dir))

    for i, res in enumerate(results):
        dir_ = plot_dir / str(i)
        dir_.mkdir()

        _plot_result(rcs_coords, wcs_coords, res, dir_)

    # Create a plot summarizing the the different runs
    objective_values = [result.fun for result in results]
    summary_file_path = plot_dir / "summary.png"
    plt.figure()
    plt.plot(range(len(objective_values)), objective_values, "ro")
    plt.ylabel("Objective value")
    plt.xlabel("Run")
    plt.title("Objective value for different x_0")
    plt.savefig(summary_file_path)


def _plot_result(
    rcs_coords,  # type: np.ndarray
    wcs_coords,  # type: np.ndarray
    result,  # type: OptimizeResult
    plot_dir,  # type: Path
):  # type: (...) -> None
    """Create some plots that illustrate the result.

    Parameters
    ----------
    rcs_coords
    wcs_coords
    result
        The result from the solver
    folder
        The folder in which the plots should be stored.

    Returns
    -------
    :obj:`str`
        The path at which the plots were stored.
    """
    import matplotlib.pyplot as plt

    origin = result.x[0:3]
    x_vec = result.x[3:6]
    y_vec = result.x[6:9]
    z_vec = np.cross(x_vec, y_vec)

    x_axis = origin + 1000 * x_vec
    y_axis = origin + 1000 * y_vec
    # z_axis = origin + 1000 * z_vec

    # Calculate the localization points in the new coordinate system
    _transformed_points = []
    for point in rcs_coords:
        _transformed_points.append(
            origin + point[0] * x_vec + point[1] * y_vec + point[2] * z_vec
        )
    transformed_points = np.array(_transformed_points)

    plt.figure()
    plt.plot(wcs_coords.T[0], wcs_coords.T[1], "bo")
    plt.plot(transformed_points.T[0], wcs_coords.T[1], "rx")
    plt.plot(origin[0], origin[1], "bx")
    plt.plot(x_axis[0], x_axis[1], "rx")
    plt.plot(y_axis[0], y_axis[1], "gx")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("X-Y projection")
    plt.savefig(plot_dir / "rcs_matching_xy.png")

    plt.figure()
    plt.plot(wcs_coords.T[0], wcs_coords.T[2], "bo")
    plt.plot(transformed_points.T[0], wcs_coords.T[2], "rx")
    plt.plot(origin[0], origin[2], "bx")
    plt.plot(x_axis[0], x_axis[2], "rx")
    plt.plot(y_axis[0], y_axis[2], "gx")
    plt.xlabel("x")
    plt.ylabel("z")
    plt.title("X-Z projection")
    plt.savefig(plot_dir / "rcs_matching_xz.png")

    plt.figure()
    plt.plot(wcs_coords.T[1], wcs_coords.T[2], "bo")
    plt.plot(transformed_points.T[1], wcs_coords.T[2], "rx")
    plt.plot(origin[1], origin[2], "bx")
    plt.plot(x_axis[1], x_axis[2], "rx")
    plt.plot(y_axis[1], y_axis[2], "gx")
    plt.xlabel("y")
    plt.ylabel("z")
    plt.title("Y-Z projection")
    plt.savefig(plot_dir / "rcs_matching_yz.png")


def arbitrary_pts_localization(
    rcs_coords,  # type: List[List[float]]
    wcs_coords,  # type: List[List[float]]
    plot_results=False,  # type: bool
    maxiter=200,  # type: int
):  # type: (...) -> List[List[float]]
    """Calculate the RCS origin frame.

    Finding the origin is formulated as an optimization problem where we want
    to find the origin and two orthonormal vectors defining the coordinate
    system. At the same time, the position of the localization points in this
    new coordinate system should match the measurements as close as possible.
    Therefore the deviation from the measurements is used as the cost function.
    The only constraints are that the x and y vector need to have length 1 and
    be orthogonal to each other.  The optimization variable is a vector with 9
    entries: X = [o, x, y] where o is the origin of the coordinate system and
    x, y the vectors spanning the x-y-plane. Each of them is a 3 dimensional
    vector.  **Important**: Ensure that the order of rcs_coords and
    measurements is identical. I.e. the i-th entry in measurements is the
    measurement of the i-th localization point.

    Parameters
    ----------
    rcs_coords
        The points where the robot endeffector was positioned to take
        measurements. These points are in the RCS.
    wcs_coords
        The measurements taken in the world coordinate system (WCS) with the
        total station. These are the coordinates of the rcs_coords in
        the WCS.

    Returns
    -------
    :obj:`list` of :obj:`list` of :obj:`float`
        A tuple of 3 vectors (lists with 3 elements) where the first represents
        the origin of the RCS, the second is the direction of the x axis and
        the third the direction of the y axis. The x and y axis are vectors
        with length 1.
    """
    # Setup the constraints
    constraints = {"type": "eq", "fun": _nonlinear_constraints}

    results = []
    slices = 4
    for i in range(slices):
        radians = np.deg2rad(360.0 / float(slices) * i)
        c, s = np.cos(radians), np.sin(radians)
        rotation = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))

        x = rotation.dot(np.array([1, 0, 0]))
        y = rotation.dot(np.array([0, 1, 0]))

        # We use the standard coordinate system as an initial guess.
        x0 = np.array(np.concatenate(([0, 0, 0], x, y)))
        res = minimize(
            _objective_function,
            x0,
            args=(rcs_coords, wcs_coords),
            method="SLSQP",  # Default method for problems with constraints
            constraints=constraints,
            options={"disp": True, "maxiter": maxiter},
        )

        results.append(res)

    if plot_results:
        _plot(rcs_coords, wcs_coords, results)

    # Pick the result with the lowest objective value
    result = reduce((lambda x, y: x if x.fun < y.fun else y), results)

    origin = result.x[0:3].tolist()
    x_vec = result.x[3:6].tolist()
    y_vec = result.x[6:9].tolist()

    return [origin, x_vec, y_vec]
