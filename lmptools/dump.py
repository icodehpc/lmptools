from __future__ import annotations
from pydantic import BaseModel, validator, parse_obj_as
from .atom import Atom
import pandas as pd
from typing import List, Dict, Optional
from loguru import logger

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

    def __str__(self):
        if self.triclinic:
            return f"{self.xlo} {self.xhi} {self.xy}\n"+f"{self.ylo} {self.yhi} {self.yz}\n"+f"{self.zlo} {self.zhi} {self.xz}"
        else:
            return f"{self.xlo} {self.xhi}\n"+f"{self.ylo} {self.yhi}\n"+f"{self.zlo} {self.zhi}\n"

class DumpSnapshot(BaseModel):
    """
    Generic class to represent a single lammps system snapshot.
    All the atom data is held in a pandas dataframe for easier processing
    """
    timestamp: int
    box: SimulationBox
    natoms: int
    atoms: List[Atom]
    unwrapped: bool = False

    @validator('atoms')
    def num_atoms_must_match_natoms(cls, v: List[Atom], values: dict, **kwargs):
        if len(v) != values['natoms']:
            raise AssertionError(f"Number of atoms read from file does not match {values['natoms']}")
        return v

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        timestep_header = "ITEM: TIMESTEP"
        num_atoms_header = "ITEM: NUMBER OF ATOMS"
        simbox_header = f"ITEM: BOX BOUNDS {self.box.xprd} {self.box.yprd} {self.box.zprd}"
        atoms_header = "ITEM: ATOMS "+" ".join([colname for colname in self.atoms.columns])
        atoms = self.atoms.to_string(header=False, index=False, index_names=False).split('\n')
        
        return f"{timestep_header}\n"+\
                f"{self.timestamp}\n"+\
                f"{num_atoms_header}\n"+\
                f"{self.natoms}\n"+\
                f"{simbox_header}\n"+\
                f"{str(self.box)}"+\
                f"{atoms_header}\n"+\
                "\n".join(atoms)

class DumpFileIterator(object):
    """
    base dumpfile iterator
    """
    def __init__(self, dump_file_name: str, unwrap: bool = False):
        self.unwrap = unwrap
        try:
            self.file = open(dump_file_name)
        except FileNotFoundError:
            logger.error(f"{dump_file_name} not found")

    def unwrapped_snapshot(self, snapshot: DumpSnapshot) -> DumpSnapshot:
        if "ix" not in snapshot.atoms.columns:
            logger.info("Periodic image flags not present in snapshot, not unwrapping ... ")
            return snapshot
        
        xprd = snapshot.box.xhi - snapshot.box.xlo
        yprd = snapshot.box.yhi - snapshot.box.ylo
        zprd = snapshot.box.zhi - snapshot.box.zlo

        snapshot.atoms["x"] += snapshot.atoms["ix"]*xprd
        snapshot.atoms["y"] += snapshot.atoms["iy"]*yprd
        snapshot.atoms["z"] += snapshot.atoms["iz"]*zprd
        return snapshot

    def read_snapshot(self) -> Optional[DumpSnapshot]:
        """
        Read the dump file and return a single snapshot
        """
        try:
            snap: dict = {}
            if self.unwrap:
                snap["unwrapped"] = True

            item = self.file.readline()
            snap['timestamp'] = int(self.file.readline().split()[0])
            self.file.readline()
            snap['natoms'] = int(self.file.readline())

            item = self.file.readline()
            words = item.split("BOUNDS ".strip())
            box_periodicities = words[1].strip().split()

             # Read in box dimensions
            box_dimensions: dict = {}
            box_dimensions['xprd'] = box_periodicities[0]
            box_dimensions['yprd'] = box_periodicities[1]
            box_dimensions['zprd'] = box_periodicities[2]
            if len(words) == 1:
                pass
            else:
                boxstr = words[1].strip()
                if "xy" in boxstr:
                    box_dimensions['triclinic'] = True

            # xlo, xhi, xy
            words = self.file.readline().split()
            if len(words) == 2:
                box_dimensions['xlo'] = float(words[0])
                box_dimensions['xhi'] = float(words[1])
                box_dimensions['xy'] = 0.0
            else:
                box_dimensions['xlo'] = float(words[0])
                box_dimensions['xhi'] = float(words[1])
                box_dimensions['xy'] = float(words[2])

            # ylo, yhi, xz
            words = self.file.readline().split()
            if len(words) == 2:
                box_dimensions['ylo'] = float(words[0])
                box_dimensions['yhi'] = float(words[1])
                box_dimensions['xz'] = 0.0
            else:
                box_dimensions['ylo'] = float(words[0])
                box_dimensions['yhi'] = float(words[1])
                box_dimensions['xz'] = float(words[2])

            # zlo, zhi, yz
            words = self.file.readline().split()
            if len(words) == 2:
                box_dimensions['zlo'] = float(words[0])
                box_dimensions['zhi'] = float(words[1])
                box_dimensions['yz'] = 0.0
            else:
                box_dimensions['zlo'] = float(words[0])
                box_dimensions['zhi'] = float(words[1])
                box_dimensions['yz'] = float(words[2])

            snap['box'] = SimulationBox(**box_dimensions)

            atoms: List[Atom] = []
            if snap['natoms']:
                item = self.file.readline()
                keys = item.split()[2:]

                for _ in range(0, snap['natoms']):
                    row = {}
                    for key, value in zip(keys, self.file.readline().split()):
                        row[key] = float(value)
                    atoms.append(parse_obj_as(Atom, row))
            snap['atoms'] = atoms

            if self.unwrap:
                return self.unwrapped_snapshot(parse_obj_as(DumpSnapshot, snap))
            else:
                return parse_obj_as(DumpSnapshot, snap)
        except Exception as e:
            logger.exception(e)
            return None

    def __iter__(self):
        return self

    def __next__(self) -> DumpSnapshot:
        while True:
            snapshot = self.read_snapshot()
            if snapshot:
                logger.info(f"Parsed snapshot for t = {snapshot.timestamp}")
                return snapshot
            else:
                raise StopIteration()