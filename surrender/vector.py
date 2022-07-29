import numpy as np
from surrender.math_transforms import (
    translation_matrix,
    scale_matrix,
    rotation_matrix_x,
    rotation_matrix_y,
    rotation_matrix_z,
)

# new_vector_functions
def vector(x=0, y=0, z=0):
    return np.array((x,y,z))


HANDLED_FUNCTIONS = {}


def implements(np_function):
    def decorator(func):
        HANDLED_FUNCTIONS[np_function] = func
        return func

    return decorator


class Vector(np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def length(self):
        return np.linalg.norm(np.asarray(self))

    def normalized(self):
        return self / self.length()

    def apply_transform(self, matrix):
        array = np.array([self.x, self.y, self.z, 1])
        x, y, z, _ = array @ matrix
        self.x = x
        self.y = y
        self.z = z

    def move(self, vector):
        matrix = translation_matrix(vector)
        self.apply_transform(matrix)
        return self

    def scale(self, vector, around=None):
        if around is None:
            around = Vector(0, 0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        s = scale_matrix(vector)

        matrix = t0 @ s @ t1
        self.apply_transform(matrix)
        return self

    def rotate_x(self, angle, around=None):
        if around is None:
            around = Vector(0, 0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix_x(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)
        return self

    def rotate_y(self, angle, around=None):
        if around is None:
            around = Vector(0, 0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix_y(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)
        return self

    def rotate_z(self, angle, around=None):
        if around is None:
            around = Vector(0, 0)

        t0 = translation_matrix(-around)
        t1 = translation_matrix(around)
        r = rotation_matrix_z(angle)

        matrix = t0 @ r @ t1
        self.apply_transform(matrix)
        return self

    def rotate(self, delta, around=None):
        self.rotate_x(delta.x, around)
        self.rotate_y(delta.y, around)
        self.rotate_z(delta.z, around)
        return self

    def angle_with(self, other):
        if self.length() == 0 or other.length() == 0:
            return 0
        cos = np.dot(self.normalized(), other.normalized())
        angle = np.arccos(cos)
        return angle

    def x_angle(self):
        z = Vector(0, 0, 1)
        v_yz = Vector(0, self.y, self.z)
        angle = v_yz.angle_with(z)
        return angle if self.y >= 0 else -angle

    def y_angle(self):
        x = Vector(1, 0, 0)
        v_zx = Vector(self.x, 0, self.z)
        angle = v_zx.angle_with(x)
        return angle if self.z >= 0 else -angle

    def z_angle(self):
        y = Vector(0, 1, 0)
        v_xy = Vector(self.x, self.y, 0)
        angle = v_xy.angle_with(y)
        return angle if self.x >= 0 else -angle

    @implements(np.cross)
    def cross(a, b, **kwargs):
        a = np.asarray(a)
        b = np.asarray(b)
        x, y, z = np.cross(a, b, **kwargs)
        return Vector(x, y, z)

    @implements(np.dot)
    def dot(a, b, **kwargs):
        a = np.asarray(a)
        b = np.asarray(b)
        return np.dot(a, b, **kwargs)

    @implements(np.append)
    def append(array, values, axis=None):
        a = np.asarray(array)
        return np.append(a, values, axis=axis)

    def copy(self):
        return self.__class__(self.x, self.y, self.z)

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f"Vector({self.x :.2f}, {self.y :.2f}, {self.z :.2f})"

    def __array__(self, dtype=None):
        return np.array([self.x, self.y, self.z], dtype=dtype)

    def __array_ufunc__(self, ufunc, method, *args, **kwargs):
        out = kwargs.get("out", None)
        kwargs["out"] = None

        if method == "__call__":
            inputs = [np.asarray(i) for i in args]
            x, y, z = ufunc(*inputs, **kwargs)
            result = self.__class__(x, y, z)

            if out is None:
                return result

            for i in out:
                if isinstance(i, np.ndarray):
                    i[:3] = x, y, z
                elif isinstance(i, __class__):
                    i.x, i.y, i.z = x, y, z
                else:
                    return NotImplemented
            return result

        else:
            return NotImplemented

    def __array_function__(self, func, types, args, kwargs):
        if func not in HANDLED_FUNCTIONS:
            return NotImplemented

        if not all(issubclass(t, self.__class__) for t in types):
            return NotImplemented

        return HANDLED_FUNCTIONS[func](*args, **kwargs)
