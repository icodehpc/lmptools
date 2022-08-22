from typing import List

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from lmptools.core.simulation import DumpSnapshot

from ..base import SnapshotWriter
from .models import AtomModel, Base, SimulationBoxModel, SimulationModel, TimestepModel


class SQLWriter(SnapshotWriter):
    """
    Special callback to insert snapshot into a sqlite database

    Overrides the on_snapshot_parse_end method to insert the snapshot into database
    """

    def __init__(self, simulation_id: int, db_name: str = "snapshots.db", debug: bool = False):
        self.__db_name = db_name
        if debug:
            self.__engine = create_engine(f"sqlite:///{self.__db_name}", echo=True)
        else:
            self.__engine = create_engine(f"sqlite:///{self.__db_name}", echo=False)

        self.__session = Session(bind=self.__engine)
        Base.metadata.create_all(bind=self.__engine)
        self.__simulation_id = simulation_id
        self.__debug = debug

        # Persist the simulation
        self.__sim = SimulationModel(id=self.__simulation_id)
        try:
            self.__session.add(self.__sim)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            if self.__debug:
                logger.debug(e)

    def on_snapshot_parse_end(self, snapshot: DumpSnapshot, *args, **kwargs):
        # Add snapshot timestep into db
        timestep = TimestepModel(timestep=snapshot.timestamp, simulation=self.__sim)
        try:
            self.__session.add(timestep)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            if self.__debug:
                logger.debug(e)

        # Add simulation box info to db
        sbox = SimulationBoxModel(simulation=self.__sim, timestep=timestep)
        for field in snapshot.box.__fields_set__:
            sbox.__dict__[field] = snapshot.box.__dict__[field]

        try:
            self.__session.add(sbox)
            self.__session.commit()
        except Exception:
            self.__session.rollback()

        # Insert atoms
        atom_models: List[AtomModel] = []
        for atom in snapshot.atoms:
            atom_model = AtomModel(simulation=self.__sim, timestep=timestep)
            for field in atom.__fields_set__:
                atom_model.__dict__[field] = atom.__dict__[field]
            atom_models.append(atom_model)

        try:
            self.__session.bulk_save_objects(atom_models, return_defaults=True)
            self.__session.commit()
        except Exception:
            self.__session.rollback()

        if self.__debug:
            logger.debug(f"Snapshot {snapshot.timestamp} inserted into {self.__db_name}")
