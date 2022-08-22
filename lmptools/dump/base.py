from __future__ import annotations

from typing import List, Optional

from loguru import logger
from pydantic import parse_obj_as

from ..core.atom import Atom
from ..core.exceptions import SkipSnapshot
from ..core.simulation import DumpSnapshot, SimulationBox


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


class CallbackList(DumpCallback):
    """
    Container to wrap multiple callbacks. Provides a cleaner interface to invoke the callback hooks
    by invoking the function just once
    """

    def __init__(self, callbacks=None):
        self.callbacks = callbacks
        # If only a single instance is provided, wrap it as a list
        if isinstance(callbacks, DumpCallback):
            self.callbacks = [callbacks]

    def on_snapshot_parse_begin(self, *args, **kwargs):
        if self.callbacks:
            for callback in self.callbacks:
                callback.on_snapshot_parse_begin(*args, **kwargs)

    def on_snapshot_parse_timestamp(self, timestamp: int, *args, **kwargs):
        if self.callbacks:
            for callback in self.callbacks:
                callback.on_snapshot_parse_timestamp(timestamp, *args, **kwargs)

    def on_snapshot_parse_natoms(self, natoms: int, *args, **kwargs):
        if self.callbacks:
            for callback in self.callbacks:
                callback.on_snapshot_parse_natoms(natoms, *args, **kwargs)

    def on_snapshot_parse_box(self, box: SimulationBox, *args, **kwargs):
        if self.callbacks:
            for callback in self.callbacks:
                callback.on_snapshot_parse_box(box, *args, **kwargs)

    def on_snapshot_parse_atoms(self, atoms: List[Atom], *args, **kwargs):
        if self.callbacks:
            for callback in self.callbacks:
                callback.on_snapshot_parse_atoms(atoms, *args, **kwargs)

    def on_snapshot_parse_end(self, snapshot: DumpSnapshot, *args, **kwargs):
        if self.callbacks:
            for callback in self.callbacks:
                callback.on_snapshot_parse_end(snapshot, *args, **kwargs)


class Dump(object):
    """
    Base Dump class to parse LAMMPS dump files
    """

    def __init__(
        self,
        dump_file_name: str,
        unwrap: bool = False,
        callbacks: Optional[List[DumpCallback]] = None,
        verbose: bool = False,
    ):
        self.snapshot: Optional[DumpSnapshot] = None
        self.dump_file_name = dump_file_name
        self.unwrap = unwrap
        self.callbacks = CallbackList(callbacks=callbacks)
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
        item = self.file.readline()  # +1

        # Readline with return an empty string if end of file is reached
        if len(item) == 0:
            self.snapshot = None
            return

        # Invoke on_snapshot_parse_begin callback
        self.callbacks.on_snapshot_parse_begin()

        timestamp = int(self.file.readline().split()[0])  # +1
        snap["timestamp"] = timestamp

        # Invoke on_snapshot_parse_timestamp callback
        self.callbacks.on_snapshot_parse_timestamp(timestamp=timestamp)

        item = self.file.readline()
        natoms = int(self.file.readline())  # +1
        snap["natoms"] = natoms

        # Invoke on_snapshot_parse_natoms callback
        self.callbacks.on_snapshot_parse_natoms(natoms=natoms)

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
        self.callbacks.on_snapshot_parse_box(box=snap["box"])

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
            self.callbacks.on_snapshot_parse_atoms(atoms)

        # Create the snapshot
        self.snapshot = parse_obj_as(DumpSnapshot, snap)

        # Invoke on_snapshot_parse_end callback
        self.callbacks.on_snapshot_parse_end(snapshot=self.snapshot)

    def __iter__(self):
        return self

    def __next__(self) -> Optional[DumpSnapshot]:
        try:
            self.parse_snapshot()
            if self.snapshot:
                return self.snapshot
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

    def parse(self) -> None:
        """
        Method to parse all the snapshots and optionally persist in file/db
        """
        # Iterate over self while invoking the callbacks if provided
        for _ in self:
            pass
        return None
