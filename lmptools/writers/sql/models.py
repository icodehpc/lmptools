from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# Create the SQLAlchemy db models for saving snapshots to database
class SimulationModel(Base):
    """
    Top level table to encapsulate the entire simulation
    """

    __tablename__ = "simulation"
    id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    timesteps = relationship("TimestepModel", backref="simulation")
    simboxes = relationship("SimulationBoxModel", backref="simulation")
    # molecules = relationship('MoleculeModel', backref='simulation')
    atoms = relationship("AtomModel", backref="simulation")


class TimestepModel(Base):
    """
    Timesteps in a given simulation
    simulation and timesteps share a one to many relationship

    one-to-one relationship between a timestep and a simulation box
    """

    __tablename__ = "timesteps"
    timestep = Column(Integer, primary_key=True, autoincrement=False, index=True)
    simulation_id = Column(Integer, ForeignKey("simulation.id"), index=True)
    sim_box = relationship("SimulationBoxModel", backref="timestep", uselist=False)
    # molecules = relationship('MoleculeModel', backref='timestep')
    atoms = relationship("AtomModel", backref="timestep")


class SimulationBoxModel(Base):
    """
    SQLAlchemy model for writing simulation box dimensions
    """

    __tablename__ = "simulation_box"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    xprd = Column(String, default="pp")
    yprd = Column(String, default="pp")
    zprd = Column(String, default="pp")
    xlo = Column(Float, nullable=True)
    xhi = Column(Float, nullable=True)
    ylo = Column(Float, nullable=True)
    yhi = Column(Float, nullable=True)
    zlo = Column(Float, nullable=True)
    zhi = Column(Float, nullable=True)
    xy = Column(Float, nullable=True)
    xz = Column(Float, nullable=True)
    yz = Column(Float, nullable=True)
    triclinic = Column(Boolean, nullable=True, default=False)

    simulation_id = Column(Integer, ForeignKey("simulation.id"), index=True)
    timestep_id = Column(Integer, ForeignKey("timesteps.timestep"), index=True)


class AtomModel(Base):
    """
    SQLaclchemy model for a simulation atom(s)
    """

    __tablename__ = "atoms"
    sql_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, index=True)
    mol = Column(Integer, index=True)
    timestep_id = Column(Integer, ForeignKey("timesteps.timestep"), index=True)
    simulation_id = Column(Integer, ForeignKey("simulation.id"), index=True)
    type = Column(Integer, default=1, index=True)
    mass = Column(Float, default=1.0)
    x = Column(Float, nullable=True)
    xu = Column(Float, nullable=True)
    xs = Column(Float, nullable=True)
    xsu = Column(Float, nullable=True)
    y = Column(Float, nullable=True)
    yu = Column(Float, nullable=True)
    ys = Column(Float, nullable=True)
    ysu = Column(Float, nullable=True)
    z = Column(Float, nullable=True)
    zu = Column(Float, nullable=True)
    zs = Column(Float, nullable=True)
    zsu = Column(Float, nullable=True)
    q = Column(Float, nullable=True)
    radius = Column(Float, nullable=True)
    diameter = Column(Float, nullable=True)
    mux = Column(Float, nullable=True)
    muy = Column(Float, nullable=True)
    muz = Column(Float, nullable=True)
    vx = Column(Float, nullable=True)
    vy = Column(Float, nullable=True)
    vz = Column(Float, nullable=True)
    fx = Column(Float, nullable=True)
    fy = Column(Float, nullable=True)
    fz = Column(Float, nullable=True)
    omegax = Column(Float, nullable=True)
    omegay = Column(Float, nullable=True)
    omegaz = Column(Float, nullable=True)
    angmomx = Column(Float, nullable=True)
    angmomy = Column(Float, nullable=True)
    angmomz = Column(Float, nullable=True)
    torquex = Column(Float, nullable=True)
    torquey = Column(Float, nullable=True)
    torquez = Column(Float, nullable=True)
    ix = Column(Integer, nullable=True)
    iy = Column(Integer, nullable=True)
    iz = Column(Integer, nullable=True)
