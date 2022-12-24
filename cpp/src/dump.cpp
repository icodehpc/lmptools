#include "dump.h"

#include <algorithm>

#include "atom.h"
#include "simulation.h"

namespace lmptools {

DumpSnapshot::DumpSnapshot()
    : dumpStyle_{0}, timestep_{0}, natoms_{0}, box_(), atoms_{} {}

DumpSnapshot::DumpSnapshot(Int32 dumpStyle, Int64 timestep)
    : dumpStyle_(dumpStyle), timestep_(timestep) {}

DumpSnapshot::DumpSnapshot(Int32 dumpStyle, Int64 timestep, Int64 natoms,
                           const SimulationBox &box)
    : dumpStyle_(dumpStyle), timestep_(timestep), natoms_(natoms), box_(box) {
  atoms_.reserve(natoms);
}

DumpSnapshot::DumpSnapshot(Int32 dumpStyle, Int64 timestep, Int64 natoms,
                           const SimulationBox &box,
                           const std::vector<Atom> &atoms)
    : dumpStyle_(dumpStyle), timestep_(timestep), natoms_(natoms), box_(box) {
  atoms_.reserve(natoms);

  // Copy atoms
  std::copy(atoms.begin(), atoms.end(), atoms_.begin());
}

// Copy constructor
DumpSnapshot::DumpSnapshot(const DumpSnapshot &snapshot) {
  dumpStyle_ = snapshot.dumpStyle();
  timestep_ = snapshot.timestep();
  natoms_ = snapshot.natoms();
  box_ = snapshot.box();

  // Reserve space for natoms_
  atoms_.reserve(natoms_);

  std::copy(snapshot.atoms_.begin(), snapshot.atoms_.end(), atoms_.begin());
}

}  // namespace lmptools

/*lmptools::DumpSnapshot::DumpSnapshot(Int32 dumpStyle, Int64 timestep)
    : dumpStyle_(dumpStyle), timestep_(timestep) {}

lmptools::DumpSnapshot::DumpSnapshot(Int32 dumpStyle, Int64 timestep,
                                     Int64 natoms, const SimulationBox& box)
    : dumpStyle_(dumpStyle), timestep_(timestep), natoms_(natoms), box_(box) {}

lmptools::DumpSnapshot::DumpSnapshot(Int32 dumpStyle, Int64 timestep,
                                     Int64 natoms, const SimulationBox& box,
                                     const std::vector<Atom>& atoms)
    : dumpStyle_(dumpStyle),
      timestep_(timestep),
      natoms_(natoms),
      box_(box),
      atoms_(atoms) {}

// lmptools::DumpSnapshot::~DumpSnapshot() {}*/
