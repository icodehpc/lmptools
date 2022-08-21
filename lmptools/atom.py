from __future__ import annotations

import math
from typing import List, Optional

import pandas as pd
from pydantic import BaseModel


class Vector(BaseModel):
    x: float
    y: float
    z: float

    @property
    def dataframe(self):
        return pd.DataFrame.from_dict([self.dict(exclude_unset=True)])

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __eq__(self, vector: Vector) -> bool:
        return all(
            [self.__dict__[key] == vector.__dict__[key] for key in self.__fields_set__]
        )


class Atom(BaseModel):
    id: int = None
    mol: Optional[int] = None
    type: int = None
    mass: float = 1.0
    x: Optional[float] = None  # unscaled xcoordinate
    xu: Optional[float] = None  # unwrap coordinate
    xs: Optional[float] = None
    xsu: Optional[float] = None  # scaled unwrapped
    y: Optional[float] = None
    yu: Optional[float] = None
    ys: Optional[float] = None
    ysu: Optional[float] = None
    z: Optional[float] = None
    zu: Optional[float] = None
    zs: Optional[float] = None
    zsu: Optional[float] = None
    q: Optional[float] = None
    radius: Optional[float] = None
    diameter: Optional[float] = None
    mu: Optional[Vector] = None
    velocity: Optional[Vector] = None
    force: Optional[Vector] = None
    omega: Optional[Vector] = None
    angmom: Optional[Vector] = None
    torque: Optional[Vector] = None
    ix: Optional[int] = None
    iy: Optional[int] = None
    iz: Optional[int] = None
    unwrapped: bool = False

    def __str__(self):
        return " ".join(
            [
                f"{self.__dict__[key]}"
                for key in sorted(list(self.__fields_set__))
                if key != "unwrapped"
            ]
        )

    def __eq__(self, other: Atom) -> bool:
        return all([self.__dict__[k] == other.__dict__[k] for k in self.__fields_set__])

    def unwrap(self, lx: float, ly: float, lz: float) -> None:
        """
        Unwrap the atom's coordinate based the image flags provided
        """
        self.unwrapped = True
        if self.ix is not None and self.x is not None:
            self.xu = self.x + self.ix * lx

        if self.iy is not None and self.y is not None:
            self.yu = self.y + self.iy * ly

        if self.iz is not None and self.z is not None:
            self.zu = self.z + self.iz * lz
        return None

    @property
    def dataframe(self):
        return pd.DataFrame.from_dict([self.dict(exclude_unset=True)])
