from __future__ import annotations
import math
from pydantic import BaseModel
from typing import Optional, Any

class Vector(BaseModel):
    x: float
    y: float
    z: float

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

class Atom(BaseModel):
    id: int = None
    mol: Optional[int] = None
    type: int = None
    x: Optional[float] = None   # unscaled xcoordinate
    xu: Optional[float] = None  # unwrap coordinate
    xs: Optional[float] = None  # scaled coordiante
    xsu: Optional[float] = None # scaled unwrapped
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

    def __str__(self):
        return ", ".join([f"{key}: {self.__dict__[key]}" for key in self.__fields_set__])

    def __eq__(self, other: Atom) -> bool:
        return all([self.__dict__[k] == other.__dict__[k] for k in self.__fields_set__])