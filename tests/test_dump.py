from lmptools.exceptions import SkipSnapshot
import pytest
import os
import random
from typing import List
from lmptools.atom import Atom
from pydantic.tools import parse_obj_as
from lmptools import Dump, DumpSnapshot, SimulationBox, DumpCallback

class SkipSnapshotCallback(DumpCallback):
    """
    This sample callback will skip all snapshots in a dump file
    """
    def on_snapshot_parse_timestamp(self, timestamp: int):
        if timestamp:
            raise SkipSnapshot("skipping snapshot")

class OnSnapshotParseBegin(DumpCallback):
    """
    Callback to use to count the number of snapshots in a dumpfile

    Use the on_snapshot_parse_begin callback to increment the `num_snapshots` attribute by 1
    each time to count the snapshots
    """
    def __init__(self):
        self.num_snapshots: int = 0

    def on_snapshot_parse_begin(self, *args, **kwargs):
        self.num_snapshots = self.num_snapshots + 1

class OnSnapshotParseNatoms(DumpCallback):
    def __init__(self):
        self.natoms: List[int] = []

    def on_snapshot_parse_natoms(self, natoms: int, *args, **kwargs):
        self.natoms.append(natoms)

class OnSnapshotParseTimestamp(DumpCallback):
    def __init__(self):
        self.timestamps: List[int] = []

    def on_snapshot_parse_timestamp(self, timestamp: int, *args, **kwargs):
        self.timestamps.append(timestamp)

class OnSnapshotParseBox(DumpCallback):
    """
    Use this callback to cache the simulation box dimensions from each snapshot
    """
    def __init__(self):
        self.simulation_box: List[SimulationBox] = []

    def on_snapshot_parse_box(self, box: SimulationBox, *args, **kwargs):
        self.simulation_box.append(box)

class OnSnapshotParseAtoms(DumpCallback):
    def __init__(self):
        self.atoms: List[List[Atom]] = []

    def on_snapshot_parse_atoms(self, atoms: List[Atom], *args, **kwargs):
        self.atoms.append(atoms)

class OnSnapshotParseEnd(DumpCallback):
    def __init__(self):
        self.snapshots: List[DumpSnapshot] = []

    def on_snapshot_parse_end(self, snapshot: DumpSnapshot, *args, **kwargs):
        self.snapshots.append(snapshot)

@pytest.fixture(scope='session')
def dump_file():
    # Create a dump file
    filename = "dump.test.lammpstrj"
    num_timesteps = random.randint(2, 20)

    snapshots = []
    with open(filename, "w") as f:
        for _ in range(num_timesteps):
            timestep = random.randint(1000, 10000)
            num_atoms = random.randint(10, 100)
            box_length = random.random()
            xlo = -box_length
            xhi = box_length
            ylo = -box_length
            yhi = box_length
            zlo = -box_length
            zhi = box_length

            box = SimulationBox(xlo=xlo, xhi=xhi, ylo=ylo, yhi=yhi,
                                zlo=zlo, zhi=zhi, xprd='pp', yprd='pp', zprd='pp')

            dump_colnames: str = ""
            if random.random() <= 0.25:
                dump_colnames = "id type mol x y z ix iy iz"
            elif random.random() > 0.25 or random.random() <= 0.5:
                dump_colnames = "id type mol x xu xsu yu z ix iy"
            else:
                dump_colnames = "id type mol x y zu zs z"

            f.write("ITEM: TIMESTEP\n")
            f.write(f"{timestep}\n")
            f.write("ITEM: NUMBER OF ATOMS\n")
            f.write(f"{num_atoms}\n")
            f.write("ITEM: BOX BOUNDS pp pp pp\n")
            f.write(f"{xlo} {xhi}\n")
            f.write(f"{ylo} {yhi}\n")
            f.write(f"{zlo} {zhi}\n")

            f.write(f"ITEM: ATOMS {dump_colnames}\n")
            atoms: List[Atom] = []
            for _ in range(num_atoms):
                entry = {}
                random_numbers = [random.random()+random.randint(100, 1000) for _ in range(len(dump_colnames))]
                for key, value in zip(dump_colnames.split(), random_numbers):
                    entry[key] = value
                atom = parse_obj_as(Atom, entry)
                atoms.append(atom)
                f.write(" ".join([str(atom.__dict__[key]) for key in dump_colnames.split()])+"\n")

            snapshots.append(DumpSnapshot(timestamp=timestep, natoms=num_atoms, box=box, atoms=atoms, unwrapped=False))
    f.close()
    yield {'filename': filename, 'snapshots': snapshots}
    os.remove("dump.test.lammpstrj")

def test_dump_snapshot_parse_iteration(dump_file):
    d = Dump(dump_file['filename'], unwrap=True)
    for index, snapshot in enumerate(d):
        assert snapshot == dump_file['snapshots'][index]

def test_dump_callback_on_snapshot_begin_parse(dump_file):
    """
    Test whether the on snapshot parse begin callback has been invoked
    """
    cb = OnSnapshotParseBegin()
    d = Dump(dump_file['filename'], callback=cb)
    d.parse()
    assert cb.num_snapshots == len(dump_file['snapshots'])

def test_dump_callback_on_snapshot_parse_timestamp(dump_file):
    """
    Test whether on_snapshot_parse_atoms callback has been invoked
    """
    cb = OnSnapshotParseTimestamp()
    d = Dump(dump_file['filename'], callback=cb)
    d.parse()

    for index, snapshot in enumerate(dump_file['snapshots']):
        assert cb.timestamps[index] == snapshot.timestamp

def test_dump_callback_on_snapshot_parse_natoms(dump_file):
    """
    Test whether on_snapshot_parse_atoms callback has been invoked
    """
    cb = OnSnapshotParseNatoms()
    d = Dump(dump_file['filename'], callback=cb)
    d.parse()

    for index, snapshot in enumerate(dump_file['snapshots']):
        assert cb.natoms[index] == snapshot.natoms

def test_dump_callback_on_snapshot_parse_box(dump_file):
    """
    Assert that on_snapshot_parse_box callback is called
    """
    cb = OnSnapshotParseBox()
    d = Dump(dump_file['filename'], callback=cb)
    d.parse()

    for index, snapshot in enumerate(dump_file['snapshots']):
        assert cb.simulation_box[index] == snapshot.box

def test_dump_callback_on_snapshot_parse_atoms(dump_file):
    """
    assert on_snapshot_parse_atoms is called
    """
    cb = OnSnapshotParseAtoms()
    d = Dump(dump_file['filename'], callback=cb)
    d.parse()

    for index, snapshot in enumerate(dump_file['snapshots']):
        assert cb.atoms[index] == snapshot.atoms


def test_dump_callback_on_snapshot_parse_end(dump_file):
    """
    Assert on_snapshot_parse_end is called
    """
    cb = OnSnapshotParseEnd()
    d = Dump(dump_file['filename'], callback=cb)
    d.parse()

    for index, snapshot in enumerate(dump_file['snapshots']):
        assert cb.snapshots[index] == snapshot
    
def test_dump_skip_snapshot(dump_file):
    cb = SkipSnapshotCallback()
    d = Dump(dump_file['filename'], callback=cb, persist=True)
    snapshots = d.parse()
    assert snapshots == []