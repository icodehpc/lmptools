from lmptools.sql_models import AtomModel, Base, SimulationModel, TimestepModel, SimulationBoxModel
from lmptools.dump import DumpSnapshot, SimulationBox
from lmptools.atom import Atom
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from pydantic import parse_obj_as
import numpy as np
import pytest
import random
import os


@pytest.fixture
def sql_session():
    engine = create_engine('sqlite://', echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


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

def test_create_simulation(sql_session):
    sim1 = SimulationModel(id = 1)
    sim2 = SimulationModel(id = 2)
    sql_session.add(sim1)
    sql_session.add(sim2)

    # Query db for a simulation
    num_simulations = sql_session.query(SimulationModel).count()
    assert num_simulations == 2

def test_create_simulation_and_timestep(sql_session):
    sql_session.rollback()
    sim = SimulationModel(id = 1)
    sql_session.add(sim)
    timestep = TimestepModel(timestep = 1000, simulation = sim)
    sql_session.add(timestep)

    tstep = sql_session.query(TimestepModel).first()
    assert tstep.timestep == 1000

def test_create_simulation_timestep_and_box(sql_session):
    sim = SimulationModel(id = 1)
    sql_session.add(sim)
    timestep = TimestepModel(timestep = 1000, simulation = sim)
    sql_session.add(timestep)
    box = SimulationBoxModel(xlo=-10, xhi=10, ylo=-10, yhi=10, simulation=sim, timestep=timestep)
    sql_session.add(box)

    box_res = sql_session.query(SimulationBoxModel).filter(TimestepModel.timestep == 1000).one()
    assert box_res.xlo == -10 and box_res.xhi == 10 \
            and box_res.ylo == -10 and box_res.yhi == 10 \
                and box_res.zlo == None and box_res.zhi == None

def test_create_simulation_timestep_box_molecule_and_atom(sql_session):
    sim = SimulationModel(id = 1)
    sql_session.add(sim)
    timestep = TimestepModel(timestep = 1000, simulation = sim)
    sql_session.add(timestep)
    box = SimulationBoxModel(xlo=-10, xhi=10, ylo=-10, yhi=10, simulation=sim, timestep=timestep)
    sql_session.add(box)
    atom = AtomModel(id = 1, type = 1, x = 0.1, y = 0.2, z = 0.3, timestep = timestep, simulation = sim)
    sql_session.add(atom)

    res = sql_session.query(AtomModel).one()
    assert res.type == 1 and res.x == 0.1 and res.y == 0.2 and res.z == 0.3