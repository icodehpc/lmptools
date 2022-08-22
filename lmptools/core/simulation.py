from __future__ import annotations

from typing import List, Optional

import pandas as pd
from pydantic import BaseModel, validator

from .atom import Atom


class SimulationBox(BaseModel):
    """
    Lammps simulation box dimensions
    """

    xprd: str
    yprd: str
    zprd: str
    xlo: float
    xhi: float
    ylo: float
    yhi: float
    zlo: float
    zhi: float
    xy: float = 0.0
    xz: float = 0.0
    yz: float = 0.0
    triclinic: bool = False

    @property
    def Lx(self):
        return self.xhi - self.xlo

    @property
    def Ly(self):
        return self.yhi - self.ylo

    @property
    def Lz(self):
        return self.zhi - self.zlo

    def __eq__(self, other: SimulationBox) -> bool:
        return all([self.__dict__[key] == other.__dict__[key] for key in self.__fields_set__])

    def __str__(self):
        if self.triclinic:
            return (
                f"{self.xlo} {self.xhi} {self.xy}\n"
                + f"{self.ylo} {self.yhi} {self.yz}\n"
                + f"{self.zlo} {self.zhi} {self.xz}"
            )
        else:
            return f"{self.xlo} {self.xhi}\n" + f"{self.ylo} {self.yhi}\n" + f"{self.zlo} {self.zhi}\n"


class DumpSnapshot(BaseModel):
    """
    Generic class to represent a single lammps system snapshot.
    All the atom data is held in a pandas dataframe for easier processing
    """

    timestamp: Optional[int] = None
    natoms: Optional[int] = None
    box: Optional[SimulationBox] = None
    atoms: Optional[List[Atom]] = None
    unwrapped: bool = False

    @validator("atoms")
    def num_atoms_must_match_natoms(cls, v: List[Atom], values: dict, **kwargs):
        if len(v) != values["natoms"]:
            raise AssertionError(f"Number of atoms read from file does not match {values['natoms']}")
        return v

    class Config:
        arbitrary_types_allowed = True

    def __eq__(self, snapshot: DumpSnapshot) -> bool:
        """
        Check if snapshots match
        """
        return all(
            [
                self.timestamp == snapshot.timestamp,
                self.box == snapshot.box,
                self.natoms == snapshot.natoms,
            ]
        )

    def __str__(self):
        timestep_header = "ITEM: TIMESTEP"
        num_atoms_header = "ITEM: NUMBER OF ATOMS"
        simbox_header = f"ITEM: BOX BOUNDS {self.box.xprd} {self.box.yprd} {self.box.zprd}"
        atoms_header = "ITEM: ATOMS " + " ".join(
            sorted([colname for colname in self.atoms[0].__fields_set__ if colname != "unwrapped"])
        )
        atoms = "\n".join([str(atom) for atom in self.atoms]).split("\n")

        return (
            f"{timestep_header}\n"
            + f"{self.timestamp}\n"
            + f"{num_atoms_header}\n"
            + f"{self.natoms}\n"
            + f"{simbox_header}\n"
            + f"{str(self.box)}"
            + f"{atoms_header}\n"
            + "\n".join(atoms)
        )

    def __add__(self, snapshot: DumpSnapshot):
        """
        Add atoms from `snapshot` with `self` while making sure that the timesteps are exactly the same
        """
        assert snapshot.timestamp == self.timestamp
        assert snapshot.box == self.box
        atoms = self.atoms + snapshot.atoms
        unwrapped = True if self.unwrapped and snapshot.unwrapped else False
        return DumpSnapshot(
            timestamp=self.timestamp,
            natoms=self.natoms + snapshot.natoms,
            box=self.box,
            atoms=atoms,
            unwrapped=unwrapped,
        )

    @property
    def dataframe(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict([atom.dict(exclude_unset=True) for atom in self.atoms])
