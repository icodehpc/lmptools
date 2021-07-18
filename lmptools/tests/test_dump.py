import pytest
import os
import random
import pandas as pd
from lmptools.dump import DumpFileIterator, SimulationBox

@pytest.fixture(scope='session')
def dump_file():
    # Create a dump file
    filename = "dump.test.lammpstrj"
    timestep = random.randint(1000, 10000)
    num_atoms = random.randint(10, 100)
    box_length = random.random()
    xlo = -box_length
    xhi = box_length
    ylo = -box_length
    yhi = box_length
    zlo = -box_length
    zhi = box_length

    dump_columns: str = ""
    if random.random() <= 0.25:
        dump_columns = "id type mol x y z ix iy iz"
    elif random.random() > 0.25 or random.random() <= 0.5:
        dump_columns = "id type mol x xu xsu yu z ix iy"
    else:
        dump_columns = "id type mol x y zu zs z"

    with open(filename, "w") as f:
        f.write("ITEM: TIMESTEP\n")
        f.write(f"{timestep}\n")
        f.write("ITEM: NUMBER OF ATOMS\n")
        f.write(f"{num_atoms}\n")
        f.write("ITEM: BOX BOUNDS pp pp pp\n")
        f.write(f"{xlo} {xhi}\n")
        f.write(f"{ylo} {yhi}\n")
        f.write(f"{zlo} {zhi}\n")

        f.write(f"ITEM: ATOMS {dump_columns}\n")
        atoms = []
        for _ in range(num_atoms):
            entry = {}
            for key, value in zip(dump_columns.split(), [random.random() for _ in range(len(dump_columns))]):
                entry[key] = value
            atoms.append(entry)
            f.write(" ".join([str(value) for value in entry.values()])+"\n")
    f.close()
    atoms_df = pd.DataFrame.from_dict(atoms)
    yield {'filename': filename, 'timestamp': timestep, 'natoms': num_atoms,
            'box': SimulationBox(xlo=xlo, xhi=xhi, ylo=ylo, yhi=yhi, zlo=zlo, zhi=zhi, xprd='pp', yprd='pp', zprd='pp'),
            'atoms': atoms_df}

    os.remove("dump.test.lammpstrj")


def test_dump_snapshot_parse(dump_file):
    d = DumpFileIterator(dump_file['filename'])
    snapshot = d.read_snapshot()
    
    assert snapshot.natoms == dump_file['natoms']
    assert snapshot.timestamp == dump_file['timestamp']
    assert snapshot.box == dump_file['box']
    assert snapshot.atoms.equals(dump_file['atoms']) == True