"""
This modules contains all the geometry need to make any kind of cross-section.
You can use directly the function ```regular_polygon``` and the transformations
like ```move```, ```rotate``` and ```scale``` to model your desired curve.

You can assemble JordanCurves to create shapes with holes,
or even unconnected shapes.
"""

import numpy as np


class JordanCurve:
    """
    Jordan Curve is an arbitrary closed curve which doesn't intersect itself.
    It stores a set of points, and by connecting these points it's possible
    to create any polygon.
    """

    def __init__(self, points: np.ndarray) -> None:
        points = np.array(points)
        self.points = points

    def __neg__(self):
        return self.__class__(self.points[::-1])

    def move(self, horizontal: float = 0, vertical: float = 0):
        """
        Move all the curve by an amount of (x, y)
        Example: move(1, 2)
            (0, 0) becomes (1, 2)
            (1, 2) becomes (2, 4)
            (1, 0) becomes (2, 2)
        """
        self.points[:, 0] += horizontal
        self.points[:, 1] += vertical
        return self

    def rotate_radians(self, angle: float):
        """
        Rotates counter-clockwise by an amount of 'angle' in radians
        Example: rotate(pi/2)
            (1, 0) becomes (0, 1)
            (2, 3) becomes (-3, 2)
        """
        cossinus, sinus = np.cos(angle), np.sin(angle)
        rotation_matrix = cossinus * np.eye(2)
        rotation_matrix[0, 1] = sinus
        rotation_matrix[1, 0] = -sinus
        for i, point in enumerate(self.points):
            self.points[i] = rotation_matrix @ point
        return self

    def rotate_degrees(self, angle: float):
        """
        Rotates counter-clockwise by an amount of 'angle' in degrees
        Example: rotate(90)
            (1, 0) becomes (0, 1)
            (2, 3) becomes (-3, 2)
        """
        return self.rotate_radians(np.pi * angle / 180)

    def scale(self, horizontal: float = 1, vertical: float = 1):
        """
        Scales the current curve by 'x' in x-direction and 'y' in y-direction
        Example: scale(1, 2)
            (1, 0) becomes (1, 0)
            (1, 3) becomes (1, 6)
        """
        self.points[:, 0] *= horizontal
        self.points[:, 1] *= vertical
        return self

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other) -> bool:
        """
        Verify if the polygon is equal.
        Two jordan curves have the boundary points
        """
        if not isinstance(other, JordanCurve):
            error_msg = f"You must compare two Jordan, not {type(other)}"
            raise TypeError(error_msg)
        geometric_tolerance = 1e-6
        npts = self.points.shape[0] - 1
        if npts != other.points.shape[0] - 1:
            return False
        j = 0  # Track index of other
        while True:
            distance_square = np.sum((other.points[j] - self.points[0]) ** 2)
            if distance_square < geometric_tolerance:
                break
            j += 1
            if j == npts:  # There's no match
                return False
        print("j = ", j)
        for i in range(npts):
            point0, point1 = self.points[i], other.points[(i + j) % npts]
            distance_square = np.sum((point1 - point0) ** 2)
            if distance_square > geometric_tolerance:
                return False
        return True


class Shape:
    """
    An arbitrary 2D shape
    Methods:
        C = A + B : union (C = A cup B)
        C = A * B : intersection (C = A cap B)
        C = A - B : C = A - (A*B)
        C = B - A : C = B - (A*B)
        C = A ^ B : C = (A+B) - (A*B)

    Methods:
        move
        rotate
        scale (x or y or both)
    """

    def __init__(self, curves):
        self.curves = curves

    def move(self, horizontal: float = 0, vertical: float = 0):
        """
        Move all the curve by an amount of (x, y)
        Example: move(1, 2)
            (0, 0) becomes (1, 2)
            (1, 2) becomes (2, 4)
            (1, 0) becomes (2, 2)
        """
        for curve in self.curves:
            curve.move(horizontal, vertical)
        return self

    def rotate_radians(self, angle: float):
        """
        Rotates counter-clockwise by an amount of 'angle' in radians
        Example: rotate(pi/2)
            (1, 0) becomes (0, 1)
            (2, 3) becomes (-3, 2)
        """
        for curve in self.curves:
            curve.rotate_radians(angle)
        return self

    def rotate_degrees(self, angle: float):
        """
        Rotates counter-clockwise by an amount of 'angle' in degrees
        Example: rotate(90)
            (1, 0) becomes (0, 1)
            (2, 3) becomes (-3, 2)
        """
        for curve in self.curves:
            curve.rotate_degrees(angle)
        return self

    def scale(self, horizontal: float = 1, vertical: float = 1):
        """
        Scales the current curve by 'x' in x-direction and 'y' in y-direction
        Example: scale(1, 2)
            (1, 0) becomes (1, 0)
            (1, 3) becomes (1, 6)
        """
        for curve in self.curves:
            curve.scale(horizontal, vertical)
        return self

    def __add__(self, other_shape):
        raise NotImplementedError

    def __sub__(self, other_shape):
        raise NotImplementedError

    def __mul__(self, other_shape):
        raise NotImplementedError

    def __xor__(self, other_shape):
        raise NotImplementedError

    def __neg__(self):
        new_curves = []
        for curve in self.curves:
            new_curves.append(-curve)
        return Shape(new_curves)

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        if not isinstance(other, Shape):
            error_msg = f"You must compare two Shape, not {type(other)}"
            raise TypeError(error_msg)
        for curve1, curve2 in zip(self.curves, other.curves):
            if curve1 != curve2:
                return False
        return True


def regular_polygon(nsides: int):
    """
    Creates a regular polygon of n-sides inscribed in a circle of radius 1.
        if nsides = 3, it's a triangle
        if nsides = 4, it's a square, of side square(2)
    """
    if not isinstance(nsides, int):
        raise TypeError("nsides must be an integer")
    if nsides < 3:
        raise ValueError("nsides must be >= 3")
    points = np.empty((nsides + 1, 2), dtype="float64")
    theta = np.linspace(0, 2 * np.pi, nsides + 1)
    points[:, 0] = np.cos(theta)
    points[:, 1] = np.sin(theta)
    curve = JordanCurve(points)
    return Shape([curve])
