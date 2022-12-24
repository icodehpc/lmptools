#ifndef DUMP_H_
#define DUMP_H_

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
 * */
class DumpSnapshot {
 public:
  DumpSnapshot();
  DumpSnapshot(Int32 dumpStyle, Int64 timestep);

  DumpSnapshot(Int32 dumpStyle, Int64 timestep, Int64 natoms,
               const SimulationBox &box);

  DumpSnapshot(Int32 dumpStyle, Int64 timestep, Int64 natoms,
               const SimulationBox &box, const std::vector<Atom> &atoms);

  //  ~DumpSnapshot();

  // Copy constructor
  DumpSnapshot(const DumpSnapshot &snapshot);

  // Move constructor
  DumpSnapshot(const DumpSnapshot &&snapshot);

  // Add atoms
  void append(const Atom &atom);

  // Subscript operator (read/write)
  const Atom &operator[](Int64 index) const;
  Atom &operator[](Int64 index);

  // Getters and setters
  const auto &dumpStyle() const { return dumpStyle_; }
  auto &dumpStyle() {
    return const_cast<decltype(dumpStyle_) &>(
        const_cast<const DumpSnapshot *>(this)->dumpStyle());
  }

  const auto &timestep() const { return timestep_; }
  auto &timestep() {
    return const_cast<decltype(timestep_) &>(
        const_cast<const DumpSnapshot *>(this)->timestep());
  }

  const auto &natoms() const { return natoms_; }
  auto &natoms() {
    return const_cast<decltype(natoms_) &>(
        const_cast<const DumpSnapshot *>(this)->natoms());
  }

  const auto &box() const { return box_; }
  auto &box() {
    return const_cast<decltype(box_) &>(
        const_cast<const DumpSnapshot *>(this)->box());
  }

  const Atom &atom(Int64 id) const { return atoms_[id]; };

 private:
  Int32 dumpStyle_;
  Int64 timestep_;
  Int64 natoms_;
  SimulationBox box_;
  std::vector<Atom> atoms_;
};

}  // namespace lmptools

#endif
