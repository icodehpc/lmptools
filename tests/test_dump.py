from lmptools.exceptions import SkipSnapshot
import pytest
import os
import random
import pandas as pd
from typing import List
from lmptools.atom import Atom
from pydantic.tools import parse_obj_as
from lmptools import Dump, DumpFileIterator, DumpSnapshot, SimulationBox, DumpCallback, DumpMetadata

class TestCallback(DumpCallback):
    def on_snapshot_parse_time(self, timestamp: int, *args, **kwargs):
        print(f"timestamp: {timestamp} parsed")

class SkipSnapshotCallback(DumpCallback):
    """
    This sample  callback will skip snapshot with timestamp less than 5000
    """
    def on_snapshot_parse_timestamp(self, timestamp: int):
        if timestamp < 5000:
            raise SkipSnapshot("skipping snapshot")

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
    #os.remove("dump.test.lammpstrj")


def test_dump_snapshot_parse(dump_file):
    d = DumpFileIterator(dump_file['filename'])
    for index, snapshot in enumerate(d):
        assert snapshot == dump_file['snapshots'][index]