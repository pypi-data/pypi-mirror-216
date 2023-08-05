"""A set of helper functions for using cvxpy.
"""
from __future__ import annotations
import logging
from itertools import product

import numpy as np
import cvxpy as cp
from cvxpy.expressions.variable import Variable
from cvxpy.expressions.expression import Expression

from .roc_utils import calc_cost_of_point, compute_global_roc_from_groupwise


# Maximum distance from solution to feasibility or optimality
SOLUTION_TOLERANCE = 1e-9


def compute_line(p1: np.ndarray, p2: np.ndarray) -> tuple[float, float]:
    """Computes the slope and intercept of the line that passes
    through the two given points.
    
    The intercept is the value at x=0!
    (or NaN for vertical lines)
    
    For vertical lines just use the x-value of one of the points
    to find the intercept at y=0.

    Parameters
    ----------
    p1 : np.ndarray
        A 2-D point.
    p2 : np.ndarray
        A 2-D point.

    Returns
    -------
    tuple[float, float]
        A tuple pair with (slope, intercept) of the line that goes from p1 to p2.

    Raises
    ------
    ValueError
        Raised when input is invalid, e.g., when p1 == p2.
    """

    p1x, p1y = p1
    p2x, p2y = p2
    if all(p1 == p2):
        raise ValueError("Invalid points: p1==p2;")

    # Vertical line
    if np.isclose(p2x, p1x):
        slope = np.inf
        intercept = np.nan

    # Diagonal or horizontal line
    else:
        slope = (p2y - p1y) / (p2x - p1x)
        intercept = p1y - slope * p1x

    return slope, intercept


def compute_halfspace_inequality(
        p1: np.ndarray,
        p2: np.ndarray,
    ) -> tuple[float, float, float]:
    """Computes the halfspace inequality defined by the vector p1->p2, such that
        Ax + b <= 0,
        where A and b are extracted from the line that goes through p1->p2.

    As such, the inequality enforces that points must lie on the LEFT of the 
    line defined by the p1->p2 vector.

    In other words, input points are assumed to be in COUNTER CLOCK-WISE order 
    (right-hand rule).

    Parameters
    ----------
    p1 : np.ndarray
        A point in the halfspace.
    p2 : np.ndarray
        Another point in the halfspace.

    Returns
    -------
    tuple[float, float, float]
        Returns an array of size=(n_dims + 1), with format [A; b],
        representing the inequality Ax + b <= 0.

    Raises
    ------
    RuntimeError
        Thrown in case if inconsistent internal state variables.
    """
    slope, intercept = compute_line(p1, p2)

    # Unpack the points for ease of use
    p1x, p1y = p1
    p2x, p2y = p2

    # if slope is infinity, the constraint only applies to the values of x;
    # > the halfspace's b intercept value will correspond to this value of x;
    if np.isinf(slope):

        # Sanity check for vertical line
        if not np.isclose(p1x, p2x):
            raise RuntimeError(
                "Got infinite slope for line containing two points with "
                "different x-axis coordinates.")
        
        # Vector pointing downwards? then, x >= b
        if p2y < p1y:
            return [-1, 0, p1x]
        
        # Vector pointing upwards? then, x <= b
        elif p2y > p1y:
            return [1, 0, -p1x]
        
    # elif slope is zero, the constraint only applies to the values of y;
    # > the halfspace's b intercept value will correspond to this value of y;
    elif np.isclose(slope, 0.0):

        # Sanity checks for horizontal line
        if not np.isclose(p1y, p2y) or not np.isclose(p1y, intercept):
            raise RuntimeError(
                f"Invalid horizontal line; points p1 and p2 should have same "
                f"y-axis value as intercept ({p1y}, {p2y}, {intercept}).")

        # Vector pointing leftwards? then, y <= b
        if p2x < p1x:
            return [0, 1, -p1y]
        
        # Vector pointing rightwards? then, y >= b
        elif p2x > p1x:
            return [0, -1, p1y]

    # else, we have a standard diagonal line
    else:
        
        # Vector points left?
        # then, y <= mx + b <=> -mx + y - b <= 0
        if p2x < p1x:
            return [-slope, 1, -intercept]
        
        # Vector points right?
        # then, y >= mx + b <=> mx - y + b <= 0
        elif p2x > p1x:
            return [slope, -1, intercept]
        
    logging.error(f"No constraint can be concluded from points p1={p1} and p2={p2};")
    return [0, 0, 0]


def make_cvxpy_halfspace_inequality(
        p1: np.ndarray,
        p2: np.ndarray,
        cvxpy_point: Variable,
    ) -> Expression:
    """Creates a single cvxpy inequality constraint that enforces the given 
    point, `cvxpy_point`, to lie on the left of the vector p1->p2.

    Points must be sorted in counter clock-wise order!

    Parameters
    ----------
    p1 : np.ndarray
        A point p1.
    p2 : np.ndarray
        Another point p2.
    cvxpy_point : Variable
        The cvxpy variable over which the constraint will be applied.

    Returns
    -------
    Expression
        A linear inequality constraint of type Ax + b <= 0.
    """
    x_coeff, y_coeff, b = compute_halfspace_inequality(p1, p2)
    return np.array([x_coeff, y_coeff]) @ cvxpy_point + b <= 0


def make_cvxpy_point_in_polygon_constraints(
        polygon_vertices: np.ndarray,
        cvxpy_point: Variable,
    ) -> list[Expression]:
    """Creates the set of cvxpy constraints that force the given cvxpy variable
    point to lie within the polygon defined by the given vertices.

    Parameters
    ----------
    polygon_vertices : np.ndarray
        A sequence of points that make up a polygon.
        Points must be sorted in COUNTER CLOCK-WISE order! (right-hand rule)
    cvxpy_point : cvxpy.Variable
        A cvxpy variable representing a point, over which the constraints will
        be applied.

    Returns
    -------
    list[Expression]
        A list of cvxpy constraints.
    """
    return [
        make_cvxpy_halfspace_inequality(
            polygon_vertices[i], polygon_vertices[(i+1) % len(polygon_vertices)],
            cvxpy_point,
        )
        for i in range(len(polygon_vertices))
    ]


def compute_equal_odds_optimum(
        groupwise_roc_hulls: dict[int, np.ndarray],
        fairness_tolerance: float,
        group_sizes_label_pos: np.ndarray,
        group_sizes_label_neg: np.ndarray,
        global_prevalence: float,
        false_positive_cost: float = 1.,
        false_negative_cost: float = 1.,
    ) -> tuple[np.ndarray, np.ndarray]:
    """Computes the solution to finding the optimal fair (equal odds) classifier.

    Can relax the equal odds constraint by some given tolerance.

    Parameters
    ----------
    groupwise_roc_hulls : dict[int, np.ndarray]
        A dict mapping each group to the convex hull of the group's ROC curve.
        The convex hull is an np.array of shape (n_points, 2), containing the 
        points that form the convex hull of the ROC curve, sorted in COUNTER
        CLOCK-WISE order.
    fairness_tolerance : float
        A value for the tolerance when enforcing the equal odds fairness 
        constraint, i.e., equality of TPR and FPR among groups.
    group_sizes_label_pos : np.ndarray
        The relative or absolute number of positive samples in each group.
    group_sizes_label_neg : np.ndarray
        The relative or absolute number of negative samples in each group.
    global_prevalence : float
        The global prevalence of positive samples.
    false_positive_cost : float, optional
        The cost of a FALSE POSITIVE error, by default 1.
    false_negative_cost : float, optional
        The cost of a FALSE NEGATIVE error, by default 1.

    Returns
    -------
    (groupwise_roc_points, global_roc_point) : tuple[np.ndarray, np.ndarray]
        A tuple pair, (<1>, <2>), containing:
        1: an array with the group-wise ROC points for the solution.
        2: an array with the single global ROC point for the solution.
    """
    n_groups = len(groupwise_roc_hulls)
    if n_groups != len(group_sizes_label_neg) or n_groups != len(group_sizes_label_pos):
        raise ValueError(
            f"Invalid arguments; all of the following should have the same "
            f"length: groupwise_roc_hulls, group_sizes_label_neg, group_sizes_label_pos;")

    # Group-wise ROC points
    groupwise_roc_points_vars = [
        cp.Variable(shape=2, name=f"ROC point for group {i}", nonneg=True)
        for i in range(n_groups)
    ]

    # Define global ROC point as a linear combination of the group-wise ROC points
    global_roc_point_var = cp.Variable(shape=2, name="Global ROC point", nonneg=True)
    constraints = [
        # Global FPR is the average of group FPRs weighted by LNs in each group
        global_roc_point_var[0] == group_sizes_label_neg @ np.array([p[0] for p in groupwise_roc_points_vars]),

        # Global TPR is the average of group TPRs weighted by LPs in each group
        global_roc_point_var[1] == group_sizes_label_pos @ np.array([p[1] for p in groupwise_roc_points_vars]),
    ]

    # Relaxed equal odds constraints
    # 1st option - CONSTRAINT FOR: l-inf distance between any two group's ROCs being less than epsilon
    constraints += [
        cp.norm_inf(groupwise_roc_points_vars[i] - groupwise_roc_points_vars[j]) <= fairness_tolerance
        for i, j in product(range(n_groups), range(n_groups))
        if i < j
        # if i != j
    ]

    # Constraints for points in respective group-wise ROC curves
    for idx in range(n_groups):
        constraints += make_cvxpy_point_in_polygon_constraints(
            polygon_vertices=groupwise_roc_hulls[idx],
            cvxpy_point=groupwise_roc_points_vars[idx])

    # Define cost function
    obj = cp.Minimize(calc_cost_of_point(
        fpr=global_roc_point_var[0],
        fnr=1 - global_roc_point_var[1],
        prevalence=global_prevalence,
        false_pos_cost=false_positive_cost,
        false_neg_cost=false_negative_cost,
    ))

    # Define cvxpy problem
    prob = cp.Problem(obj, constraints)

    # Run solver
    prob.solve(solver=cp.ECOS, abstol=SOLUTION_TOLERANCE, feastol=SOLUTION_TOLERANCE)
    # NOTE: these tolerances are supposed to be smaller than the default np.isclose tolerances
    # (useful when comparing if two points are the same, within the cvxpy accuracy tolerance)

    # Log solution
    logging.info(f"cvxpy solver took {prob.solver_stats.solve_time}s; status is {prob.status}.")

    if prob.status not in ["infeasible", "unbounded"]:
        # Otherwise, problem.value is inf or -inf, respectively.
        logging.info(f"Optimal solution value: {prob.value}")
        for variable in prob.variables():
            logging.info(f"Variable {variable.name()}: value {variable.value}")
    else:
        # This line should never be reached (there are always trivial fair
        # solutions in the ROC diagonal)
        raise ValueError(f"cvxpy problem has no solution; status={prob.status}")

    groupwise_roc_points = np.vstack([p.value for p in groupwise_roc_points_vars])
    global_roc_point = global_roc_point_var.value

    # Sanity check solution cost
    solution_cost = calc_cost_of_point(
        fpr=global_roc_point[0],
        fnr=1-global_roc_point[1],
        prevalence=global_prevalence,
        false_pos_cost=false_positive_cost,
        false_neg_cost=false_negative_cost,
    )

    if not np.isclose(solution_cost, prob.value):
        logging.error(
            f"Solution was found but cost did not pass sanity check! "
            f"Found solution ROC point {global_roc_point} with theoretical cost "
            f"{prob.value}, but actual cost is {solution_cost};")

    # Sanity check congruency between group-wise ROC points and global ROC point
    global_roc_from_groupwise = compute_global_roc_from_groupwise(
        groupwise_roc_points=groupwise_roc_points,
        groupwise_label_pos_weight=group_sizes_label_pos,
        groupwise_label_neg_weight=group_sizes_label_neg,
    )
    if not all(np.isclose(global_roc_from_groupwise, global_roc_point)):
        logging.error(
            f"Solution: global ROC point ({global_roc_point}) does not seem to "
            f"match group-wise ROC points; global should be "
            f"({global_roc_from_groupwise}) to be consistent with group-wise;")

    return groupwise_roc_points, global_roc_point


def _plot_polygons(polygons: list[np.ndarray]):
    from matplotlib import pyplot as plt
    fig = plt.figure(dpi=200, figsize=(5, 5))

    for i, poly in enumerate(polygons):

        # Plot ROC curve
        plt.fill(
            poly[:, 0], poly[:, 1],
            alpha=0.2,
            label=f"poly {i}",
        )
        
        plt.legend(loc='lower right')
    
    plt.plot()
