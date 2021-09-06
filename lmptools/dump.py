from __future__ import annotations
import pandas as pd
from .exceptions import SkipSnapshot
from pydantic import BaseModel, validator, parse_obj_as
from .atom import Atom
from typing import List, Optional
from loguru import logger

class DumpMetadata(BaseModel):
    timestamp: int
    natoms: int

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
            return f"{self.xlo} {self.xhi} {self.xy}\n"+f"{self.ylo} {self.yhi} {self.yz}\n"+f"{self.zlo} {self.zhi} {self.xz}"
        else:
            return f"{self.xlo} {self.xhi}\n"+f"{self.ylo} {self.yhi}\n"+f"{self.zlo} {self.zhi}\n"

class DumpSnapshot(BaseModel):
    """
    Generic class to represent a single lammps system snapshot.
    All the atom data is held in a pandas dataframe for easier processing
    """
    metadata: DumpMetadata
    box: SimulationBox
    atoms: List[Atom]
    unwrapped: bool = False

    @validator('atoms')
    def num_atoms_must_match_natoms(cls, v: List[Atom], values: dict, **kwargs):
        if len(v) != values['natoms']:
            raise AssertionError(f"Number of atoms read from file does not match {values['natoms']}")
        return v

    class Config:
        arbitrary_types_allowed = True

    def __eq__(self, snapshot: DumpSnapshot) -> bool:
        """
        Check if snapshots match
        """
        return all([self.timestamp == snapshot.timestamp,
                    self.box == snapshot.box,
                    self.natoms == snapshot.natoms])
                
    def __str__(self):
        timestep_header = "ITEM: TIMESTEP"
        num_atoms_header = "ITEM: NUMBER OF ATOMS"
        simbox_header = f"ITEM: BOX BOUNDS {self.box.xprd} {self.box.yprd} {self.box.zprd}"
        atoms_header = "ITEM: ATOMS "+" ".join([colname for colname in self.atoms[0].__fields_set__])
        atoms = "\n".join([str(atom) for atom in self.atoms]).split('\n')
        
        return f"{timestep_header}\n"+\
                f"{self.timestamp}\n"+\
                f"{num_atoms_header}\n"+\
                f"{self.natoms}\n"+\
                f"{simbox_header}\n"+\
                f"{str(self.box)}"+\
                f"{atoms_header}\n"+\
                "\n".join(atoms)

    @property
    def dataframe(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict([atom.dict(exclude_unset=True) for atom in self.atoms])

class DumpCallback(object):
    """
    Base class used to build new callbacks that will be called as the dump file is parsed

    Custom callbacks can be created by subclassing `DumpCallback` and override the method associated
    with the stage of interest
    """
    def __init__(self):
        pass

    def on_snapshot_parse_begin(self, *args, **kwargs):
        """
        Method to be called right before a new snapshot is parsed
        """
        pass

    def on_snapshot_parse_metadata(self, metadata: DumpMetadata, *args, **kwargs):
        """
        Method invoked when metadata associated with the snapshot has been parsed
        """
        pass

    def on_snapshot_parse_box(self, box: SimulationBox, *args, **kwargs):
        """
        Method called when the simulation box info is parsed
        """
        pass

    def on_snapshot_parse_atoms(self, atoms: List[Atom], *args, **kwargs):
        """
        Method called when atoms coordinates are parsed from file
        """
        pass

    def on_snapshot_parse_end(self, snapshot: DumpSnapshot, *args, **kwargs):
        """
        Method called when a snapshot has been completely parsed
        """
        pass


class DumpFileIterator(object):
    """
    base dumpfile iterator
    """
    def __init__(self, dump_file_name: str, unwrap: bool = False, callback: Optional[DumpCallback] = None):
        self.unwrap = unwrap
        self.callback = callback
        try:
            self.file = open(dump_file_name)
        except FileNotFoundError:
            logger.error(f"{dump_file_name} not found")

    def read_snapshot(self) -> Optional[DumpSnapshot]:
        """
        Read the dump file and return a single snapshot
        """
        # Invoke on_snapshot_parse_begin
        if self.callback:
            self.callback.on_snapshot_parse_begin()
            
        snap: dict = {}
        item = self.file.readline() # +1
        # Readline with return an empty string if end of file is reached
        if len(item) == 0:
            return None
        snap['timestamp'] = int(self.file.readline().split()[0]) #+1

        # Invoke on_snapshot_parse_time
        if self.callback:
            self.callback.on_snapshot_parse_time(snap['timestamp'])

        item = self.file.readline()
        snap['natoms'] = int(self.file.readline()) #+1
        # Invoke on_snapshot_parse_natoms
        if self.callback:
            self.callback.on_snapshot_parse_natoms(snap['natoms'])

        item = self.file.readline() #+1
        words = item.split("BOUNDS ")
        # Simulation box periodicity (pp, ps ..)
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
        words = self.file.readline().split() #+1
        if len(words) == 2:
            box_dimensions['xlo'] = float(words[0])
            box_dimensions['xhi'] = float(words[1])
            box_dimensions['xy'] = 0.0
        else:
            box_dimensions['xlo'] = float(words[0])
            box_dimensions['xhi'] = float(words[1])
            box_dimensions['xy'] = float(words[2])

        # ylo, yhi, xz
        words = self.file.readline().split() #+1
        if len(words) == 2:
            box_dimensions['ylo'] = float(words[0])
            box_dimensions['yhi'] = float(words[1])
            box_dimensions['xz'] = 0.0
        else:
            box_dimensions['ylo'] = float(words[0])
            box_dimensions['yhi'] = float(words[1])
            box_dimensions['xz'] = float(words[2])

        # zlo, zhi, yz
        words = self.file.readline().split() #+1
        if len(words) == 2:
            box_dimensions['zlo'] = float(words[0])
            box_dimensions['zhi'] = float(words[1])
            box_dimensions['yz'] = 0.0
        else:
            box_dimensions['zlo'] = float(words[0])
            box_dimensions['zhi'] = float(words[1])
            box_dimensions['yz'] = float(words[2])

        snap['box'] = SimulationBox(**box_dimensions)

        # Invoke on_snapshot_parse_box
        if self.callback:
            self.callback.on_snapshot_parse_box(snap['box'])

        atoms: List[Atom] = []
        if snap['natoms']:
            column_names = self.file.readline().split()[2:] #+1
            for _ in range(0, snap['natoms']):
                row = {}
                for cname, value in zip(column_names, self.file.readline().split()): # +natoms times
                    row[cname] = float(value)
                atom = parse_obj_as(Atom, row)
                # Unwrap coordinates
                if self.unwrap:
                    atom.unwrap(snap['box'].Lx, snap['box'].Ly, snap['box'].Lz)
                atoms.append(atom)

            snap['atoms'] = atoms
            snapshot = parse_obj_as(DumpSnapshot, snap)

        # Invoke on_snapshot_parse_atoms
        if self.callback:
            self.callback.on_snapshot_parse_atoms(snap['atoms'])

        # Invoke on_snapshot_parse_end
        if self.callback:
            self.callback.on_snapshot_parse_end(snapshot)
        return snapshot
        
    def __iter__(self):
        return self

    def __next__(self) -> Optional[DumpSnapshot]:
        while True:
            try:
                snapshot = self.read_snapshot()
                if snapshot:
                    return snapshot
                else:
                    raise StopIteration
            except SkipSnapshot as e:
                logger.info(f"{e}")
                for line in self.file:
                    if not 'ITEM: TIMESTEP\n' in line:
                        continue
            except StopIteration as e:
                raise StopIteration
            except Exception as e:
                logger.exception(f"{e}")
class Dump:
    """
    Convenience wrapper around the DumpFileIterator class

    Provides the parse method that will kick off parsing the entire dump file sequentially whilst taking in
    an instance of the DumpCallbacks for custom callback executions
    """

    def __init__(self, dump_file_name: str, unwrap: bool = False):
        self._unwrap = unwrap
        self._dump_file_name = dump_file_name

    def parse(self, callback: Optional[DumpCallback] = None) -> None:
        """
        Method to parse the entire dump file from start to end
        """
        for snapshot in DumpFileIterator(dump_file_name=self._dump_file_name, unwrap=self._unwrap, callback=callback):
            if snapshot:
                logger.info(f"Parsed snapshot for t = {snapshot.timestamp}")