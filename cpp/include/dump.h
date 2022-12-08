#pragma once

#include <cstdint>
#include <vector>

#include "atom.h"
#include "simulation.h"

namespace lmptools {

enum DumpStyle {
  ATOM,
  CUSTOM,
  H5MD,
  IMAGE,
  LOCAL,
  MOLFILE,
  MOVIE,
  NETCDF,
  VTK,
  XTC,
  XYZ,
  YAML
};

/*
 * Base DumpSnapshot class
 *
 * */
template <typename T>
class DumpSnapshot {
 public:
  DumpSnapshot() = default;
  DumpSnapshot(uint8_t dumpStyle, uint64_t timestep);
  DumpSnapshot(uint8_t dumpStyle, uint64_t timestep, uint64_t natoms,
               const SimulationBox &box);
  DumpSnapshot(uint8_t dumpStyle, uint64_t timestep, uint64_t natoms,
               const SimulationBox &box, const std::vector<Atom> &atoms);

  ~DumpSnapshot();

  // Copy constructor
  DumpSnapshot(const DumpSnapshot &snapshot);

  // Move constructor
  DumpSnapshot(const DumpSnapshot &&snapshot);

  // Add atoms
  void append(const Atom &atom);

  // Subscript operator (read/write)
  const Atom &operator[](uint64_t index) const;
  Atom &operator[](uint64_t index);

  // Return a range/view of selected atoms

 private:
  uint8_t dumpStyle;
  uint64_t timestep;
  uint64_t natoms;
  SimulationBox box;
  std::vector<Atom> atoms;
};

}  // namespace lmptools
