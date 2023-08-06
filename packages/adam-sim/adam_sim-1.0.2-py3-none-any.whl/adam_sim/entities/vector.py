import numpy as np
from typing import NamedTuple


class Vector(NamedTuple):
    """
    a named tuple that contains the information of a 3D free vector in space

    Attributes
    ----------
    u : float
        the value of the first element on the u-v-w axes
    v : float
        the value of the second element on the u-v-w axes
    w : float
        the value of the third element on the u-v-w axes

    Methods
    -------
    normalize(self):
        returns a normalized vector of the instance
    norm(self):
        calculates the norm of the vector
    to_numpy(self):
        converts the vector to a numpy array
    to_list(self):
        converts the vector to a list
    from_numpy(cls, vector: np.ndarray):
        converts a numpy array to a vector
    from_list(cls, vector: list):
        converts a list to a vector
    """
    u: float
    v: float
    w: float

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.u}, {self.v}, {self.w})'

    def __mul__(self, scalar: float) -> 'Vector':
        return Vector(self.u*scalar, self.v*scalar, self.w * scalar)

    def __rmul__(self, scalar: float) -> 'Vector':
        return Vector(self.u*scalar, self.v*scalar, self.w * scalar)

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.u+other.u, self.v+other.v, self.w+other.w)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.u-other.u, self.v-other.v, self.w-other.w)

    def __truediv__(self, scalar: float) -> 'Vector':
        return Vector(self.u/scalar, self.v/scalar, self.w/scalar)

    def __neg__(self) -> 'Vector':
        return Vector(-self.u, -self.v, -self.w)

    def normalize(self) -> 'Vector':
        """
        normalizes the vector so its magnitude is unitary

        Returns
        -------
        out : ~.entities.vector.Vector
            the normalized instance of the vector
        """
        length: float = np.linalg.norm(self).astype(float)
        u: float = self.u / length
        v: float = self.v / length
        w: float = self.w / length

        return Vector(u, v, w)

    def norm(self) -> float:
        """
        calculates the norm of the vector

        Returns
        -------
        out : float
            the norm of the vector
        """
        return np.linalg.norm(self).astype(float)

    def to_numpy(self) -> np.ndarray:
        """
        converts the vector to a numpy array

        Returns
        -------
        out : numpy.ndarray
            the vector as a numpy array
        """
        return np.array(self)

    def to_list(self) -> list:
        """
        converts the vector to a list

        Returns
        -------
        out : list
            the vector as a list
        """
        return [*self]

    @classmethod
    def from_numpy(cls, vector: np.ndarray) -> 'Vector':
        """
        converts a numpy array to a vector

        Parameters
        ----------
        vector : numpy.ndarray
            the vector as a numpy array

        Returns
        -------
        out : ~.entities.vector.Vector
            the vector as a Vector
        """
        return cls(*vector)

    @classmethod
    def from_list(cls, vector: list) -> 'Vector':
        """
        converts a list to a vector

        Parameters
        ----------
        vector : list
            the vector as a list

        Returns
        -------
        out : ~.entities.vector.Vector
            the vector as a Vector
        """
        return cls(*vector)
