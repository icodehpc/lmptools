#ifndef ATOM_H
#define ATOM_H

#include <map>
#include <string>

#include "utils.h"

namespace lmptools {

/*
 * Base atom class based on the LAMMPS atom style
 *
 * */
struct Atom {
  Atom() = delete;
  Atom(Int32 id, Int32 mol_id, Int32 type, const Str element, Float64 mass,
       Float64 charge, Float64 radius, Float64 diameter,
       const Vec3<Float64> &omega, const Vec3<Float64> &angmom,
       const Vec3<Float64> &torque, const Vec3<Float64> &position,
       const Vec3<Float64> &position_scaled,
       const Vec3<Float64> &position_unwrapped, const Vec3<Int32> &image_id,
       const Vec3<Float64> &velocity, const Vec3<Float64> &force,
       const Vec3<Float64> &dipole);

  // Copy constructor
  Atom(const Atom &atom) noexcept;

  // Move constructor
  Atom(const Atom &&atom) noexcept {}

  ~Atom() = default;

  // Assignment operator
  Atom &operator=(const Atom &src) noexcept;

  // Comparison
  bool operator==(const Atom &other) const noexcept;

  Int32 id, mol_id, type;
  Str element;

  Float64 mass, charge;

  // Spherical particles
  Float64 radius, diameter;

  // Angular velocity/momentum
  Vec3<Float64> omega, angmom;

  // Torque on finite sized particles
  Vec3<Float64> torque;

  // Atom coordinates
  Vec3<Float64> position, position_scaled, position_unwrapped;

  // Image ids
  Vec3<Int32> image_id;

  // Atom velocities
  Vec3<Float64> velocity;

  // Atom forces
  Vec3<Float64> force;

  // Dipole
  Vec3<Float64> dipole;
};

}  // namespace lmptools

#endif
