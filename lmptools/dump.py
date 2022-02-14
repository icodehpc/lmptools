from __future__ import annotations
import pandas as pd
import time
import numpy as np
from .exceptions import SkipSnapshot
from pydantic import BaseModel, validator, parse_obj_as
from .atom import Atom
from typing import List, Optional
from loguru import logger
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .sql_models import AtomModel, SimulationBoxModel, SimulationModel, TimestepModel
from .sql_models import Base

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
    timestamp: Optional[int] = None
    natoms: Optional[int] = None
    box: Optional[SimulationBox] = None
    atoms: Optional[List[Atom]] = None
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
        atoms_header = "ITEM: ATOMS "+" ".join(sorted([colname for colname in self.atoms[0].__fields_set__ if colname != 'unwrapped']))
        atoms = "\n".join([str(atom) for atom in self.atoms]).split('\n')

        return f"{timestep_header}\n"+\
                f"{self.timestamp}\n"+\
                f"{num_atoms_header}\n"+\
                f"{self.natoms}\n"+\
                f"{simbox_header}\n"+\
                f"{str(self.box)}"+\
                f"{atoms_header}\n"+\
                "\n".join(atoms)

    def __add__(self, snapshot: DumpSnapshot):
        """
        Add atoms from `snapshot` with `self` while making sure that the timesteps are exactly the same
        """
        assert snapshot.timestamp == self.timestamp
        assert snapshot.box == self.box
        atoms = self.atoms + snapshot.atoms
        unwrapped = True if self.unwrapped and snapshot.unwrapped else False
        return DumpSnapshot(timestamp = self.timestamp, natoms = self.natoms + snapshot.natoms,
                    box = self.box, atoms = atoms, unwrapped = unwrapped)

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

    def on_snapshot_parse_timestamp(self, timestamp: int, *args, **kwargs):
        """
        method to be called right after the snapshot timestamp is parsed
        """
        pass

    def on_snapshot_parse_natoms(self, natoms: int, *args, **kwargs):
        """
        Method to be called right after number of atoms in the snapshot is parsed
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

class Dump(object):
    """
    Base Dump class to parse LAMMPS dump files
    """
    def __init__(self, dump_file_name: str, unwrap: bool = False, callback: Optional[DumpCallback] = None,
        persist: bool = False, verbose: bool = False):
        self.snapshot: Optional[DumpSnapshot] = None
        self.dump_file_name = dump_file_name
        self.unwrap = unwrap
        self.callback = callback
        self.verbose = verbose

        try:
            self.file = open(dump_file_name)
        except FileNotFoundError:
            logger.error(f"{dump_file_name} not found")

    def parse_snapshot(self):
        """
        Read the dump file and return a single snapshot
        """
        snap: dict = {}
        item = self.file.readline() # +1
        # Readline with return an empty string if end of file is reached
        if len(item) == 0:
            self.snapshot = None
            return
        
        # Invoke on_snapshot_parse_begin callback
        if self.callback:
            self.callback.on_snapshot_parse_begin()

        timestamp = int(self.file.readline().split()[0]) #+1
        snap['timestamp'] = timestamp

        # Invoke on_snapshot_parse_timestamp callback
        if self.callback:
            self.callback.on_snapshot_parse_timestamp(timestamp)

        item = self.file.readline()
        natoms = int(self.file.readline()) #+1
        snap['natoms'] = natoms

        # Invoke on_snapshot_parse_natoms callback
        if self.callback:
            self.callback.on_snapshot_parse_natoms(natoms)

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

        # Invoke on_snapshot_parse_box callback
        if self.callback:
            self.callback.on_snapshot_parse_box(snap['box'])

        atoms: List[Atom] = []
        if natoms:
            column_names = self.file.readline().split()[2:] #+1
            for _ in range(0, natoms):
                row = {}
                for cname, value in zip(column_names, self.file.readline().split()): # +natoms times
                    row[cname] = float(value)
                atom = parse_obj_as(Atom, row)
                # Unwrap coordinates
                if self.unwrap:
                    atom.unwrap(snap['box'].Lx, snap['box'].Ly, snap['box'].Lz)
                atoms.append(atom)

            snap['atoms'] = atoms
            # Invoke on_snapshot_parse_atoms callback
            if self.callback:
                self.callback.on_snapshot_parse_atoms(atoms)

        # Create the snapshot
        self.snapshot = parse_obj_as(DumpSnapshot, snap)

        # Invoke on_snapshot_parse_end callback
        if self.callback:
            self.callback.on_snapshot_parse_end(self.snapshot)

    def __iter__(self):
        return self

    def __next__(self) -> Optional[DumpSnapshot]:
        while True:
            try:
                self.parse_snapshot()
                if self.snapshot:
                    return self.snapshot
                elif self.snapshot is None:
                    raise StopIteration
            except SkipSnapshot as e:
                if self.verbose:
                    logger.info(f"{e}")
                # Skip the remaining lines until next line starting with ITEM: TIMESTEP\n is read
                while True:
                    line = self.file.readline()
                    if line == 'ITEM: TIMESTEP\n':
                        cur_pos = self.file.tell()
                        self.file.seek(cur_pos - len('ITEM: TIMESTEP\n'))
                        break
                    elif line == '':
                        # EOF is reached
                        break
            except StopIteration as e:
                raise StopIteration

    def parse(self, persist: bool = False) -> Optional[List[DumpSnapshot]]:
        """
        Method to parse all the snapshots and optionally persist in file/db
        """
        if persist:
            return [snapshot for snapshot in self]
        else:
            # Iterate over self while invoking the callbacks if provided
            for _ in self:
                pass
            return None

    def to_sql(self, simulation_id: int, sql_connection_str: str = 'sqlite://') -> None:
        """
        Dump the snapshots to the database referenced by the connection string
        database defaults to an in memory sqlite database
        """
        engine = create_engine(sql_connection_str, echo=False)
        session = Session(bind=engine)
        Base.metadata.create_all(bind=engine)

        sim = SimulationModel(id = simulation_id)
        try:
            session.add(sim)
            session.commit()
        except Exception:
            session.rollback()

        for snapshot in self:
            start = time.time()

            # Add the simulation timestep
            timestep = TimestepModel(timestep = snapshot.timestamp, simulation = sim)
            try:
                session.add(timestep)
                session.commit()
            except Exception:
                session.rollback()

            # Insert simulation box info into DB
            sbox = SimulationBoxModel(simulation = sim, timestep = timestep)
            for field in snapshot.box.__fields_set__:
                sbox.__dict__[field] = snapshot.box.__dict__[field]
            
            try:
                session.add(sbox)
                session.commit()
            except Exception:
                session.rollback()

            # Insert atoms
            atom_models: List[AtomModel] = []
            for atom in snapshot.atoms:
                atom_model = AtomModel(simulation = sim, timestep = timestep)
                for field in atom.__fields_set__:
                    atom_model.__dict__[field] = atom.__dict__[field]
                atom_models.append(atom_model)
            
            try:
                session.bulk_save_objects(atom_models, return_defaults=True)
                session.commit()
            except Exception as e:
                logger.exception(e)

            end = time.time()
            if self.verbose:
                logger.info(f"Snapshot {snapshot.timestamp} inserted in {end-start} seconds")