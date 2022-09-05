from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import List, Optional

from loguru import logger
from pydantic import parse_obj_as

from ..core.atom import Atom
from ..core.exceptions import SkipSnapshot
from ..core.simulation import DumpSnapshot, SimulationBox


class DumpFileParser(ABC):
    """
    Base class defining the template for a LAMMPS dump file parser

    Arg(s)

    :param filename: Path to the dump file to be parsed
    :param callback: [Optional] Callback to be used during parsing
    """

    def __init__(self, filename: str, callback: DumpCallback = None, unwrap: bool = False, verbose: bool = False):
        self.filename = filename
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Dump file {filename} not found")

        self.callback = callback
        self.unwrap = unwrap
        self.verbose = verbose

        self.file = open(self.filename)

    @abstractmethod
    def parse(self) -> Optional[DumpSnapshot]:
        raise NotImplementedError

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abstractmethod
    def __next__(self) -> DumpSnapshot:
        """
        Yield the next snapshot from file
        """
        raise NotImplementedError


class DumpCallback(ABC):
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

        :param timestamp: Snapshot timestamp
        """
        pass

    def on_snapshot_parse_natoms(self, natoms: int, *args, **kwargs):
        """
        Method to be called right after number of atoms in the snapshot is parsed

        :param natoms: Number of atoms in the snapshot
        """
        pass

    def on_snapshot_parse_box(self, box: SimulationBox, *args, **kwargs):
        """
        Method called when the simulation box info is parsed

        :param box: Parsed simulation box for the snapshot
        """
        pass

    def on_snapshot_parse_atoms(self, atoms: List[Atom], *args, **kwargs):
        """
        Method called when atoms coordinates are parsed from file

        :param atoms: List of all atoms parsed from the snapshot
        """
        pass

    def on_snapshot_parse_end(self, snapshot: DumpSnapshot, *args, **kwargs):
        """
        Method called when a snapshot has been completely parsed

        :param snapshot: Dump snapshot just parsed
        """
        pass


class Dump(DumpFileParser):
    """
    Dump class to parse LAMMPS dump files
    """

    def __init__(
        self,
        filename: str,
        callback: Optional[DumpCallback] = None,
        unwrap: bool = False,
        verbose: bool = False,
    ):
        super().__init__(filename, callback, unwrap, verbose)

    def __iter__(self):
        return self

    def __next__(self) -> Optional[DumpSnapshot]:
        try:
            snapshot = self.parse_snapshot()
            if snapshot:
                return snapshot
            else:
                raise StopIteration
        except SkipSnapshot as e:
            if self.verbose:
                logger.info(f"{e}")
                # Skip the remaining lines until next line starting with ITEM: TIMESTEP\n is read
                while True:
                    line = self.file.readline()
                    if line == "ITEM: TIMESTEP\n":
                        cur_pos = self.file.tell()
                        self.file.seek(cur_pos - len("ITEM: TIMESTEP\n"))
                        break
                    elif line == "":
                        # EOF is reached
                        break

    def parse_snapshot(self) -> Optional[DumpSnapshot]:
        """
        Read the dump file and return a single snapshot
        """
        snap: dict = {}
        item = self.file.readline()  # +1

        if not item:
            return None

        # Invoke on_snapshot_parse_begin callback
        if self.callback:
            self.callback.on_snapshot_parse_begin()

        timestamp = int(self.file.readline().split()[0])  # +1
        snap["timestamp"] = timestamp

        # Invoke on_snapshot_parse_timestamp callback
        if self.callback:
            self.callback.on_snapshot_parse_timestamp(timestamp=timestamp)

        item = self.file.readline()
        natoms = int(self.file.readline())  # +1
        snap["natoms"] = natoms

        # Invoke on_snapshot_parse_natoms callback
        if self.callback:
            self.callback.on_snapshot_parse_natoms(natoms=natoms)

        item = self.file.readline()  # +1
        words = item.split("BOUNDS ")

        # Simulation box periodicity (pp, ps ..)
        box_periodicities = words[1].strip().split()

        # Read in box dimensions
        box_dimensions: dict = {}
        box_dimensions["xprd"] = box_periodicities[0]
        box_dimensions["yprd"] = box_periodicities[1]
        box_dimensions["zprd"] = box_periodicities[2]
        if len(words) == 1:
            pass
        else:
            boxstr = words[1].strip()
            if "xy" in boxstr:
                box_dimensions["triclinic"] = True

        # xlo, xhi, xy
        words = self.file.readline().split()  # +1
        if len(words) == 2:
            box_dimensions["xlo"] = float(words[0])
            box_dimensions["xhi"] = float(words[1])
            box_dimensions["xy"] = 0.0
        else:
            box_dimensions["xlo"] = float(words[0])
            box_dimensions["xhi"] = float(words[1])
            box_dimensions["xy"] = float(words[2])

        # ylo, yhi, xz
        words = self.file.readline().split()  # +1
        if len(words) == 2:
            box_dimensions["ylo"] = float(words[0])
            box_dimensions["yhi"] = float(words[1])
            box_dimensions["xz"] = 0.0
        else:
            box_dimensions["ylo"] = float(words[0])
            box_dimensions["yhi"] = float(words[1])
            box_dimensions["xz"] = float(words[2])

        # zlo, zhi, yz
        words = self.file.readline().split()  # +1
        if len(words) == 2:
            box_dimensions["zlo"] = float(words[0])
            box_dimensions["zhi"] = float(words[1])
            box_dimensions["yz"] = 0.0
        else:
            box_dimensions["zlo"] = float(words[0])
            box_dimensions["zhi"] = float(words[1])
            box_dimensions["yz"] = float(words[2])

        snap["box"] = SimulationBox(**box_dimensions)

        # Invoke on_snapshot_parse_box callback
        if self.callback:
            self.callback.on_snapshot_parse_box(box=snap["box"])

        atoms: List[Atom] = []
        if natoms:
            column_names = self.file.readline().split()[2:]  # +1
            for _ in range(0, natoms):
                row = {}
                for cname, value in zip(column_names, self.file.readline().split()):  # +natoms times
                    row[cname] = float(value)
                atom = parse_obj_as(Atom, row)
                # Unwrap coordinates
                if self.unwrap:
                    atom.unwrap(snap["box"].Lx, snap["box"].Ly, snap["box"].Lz)
                atoms.append(atom)

            snap["atoms"] = atoms
            # Invoke on_snapshot_parse_atoms callback
            if self.callback:
                self.callback.on_snapshot_parse_atoms(atoms)

        # Create the snapshot
        snapshot = parse_obj_as(DumpSnapshot, snap)

        # Invoke on_snapshot_parse_end callback
        if self.callback:
            self.callback.on_snapshot_parse_end(snapshot=snapshot)

        return snapshot

    def parse(self) -> None:
        """
        Method to parse all the snapshots and optionally persist in file/db
        """
        # Iterate over self while invoking the callbacks if provided
        for _ in self:
            pass
        return None
