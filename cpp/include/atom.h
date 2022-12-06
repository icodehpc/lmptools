#ifndef ATOM_H
#define ATOM_H

#include <string>

#include "utils.h"

namespace lmptools {

/*
 * Base atom class based on the LAMMPS atom style
 *
 * */
class Atom {
 public:
  Atom() = delete;
  Atom(Int32 atomID, Int32 molID, Int32 type, const Str element, Float64 mass,
       Float64 charge, Float64 radius, Float64 diameter,
       const Vec3<Float64> &omega, const Vec3<Float64> &angmom,
       const Vec3<Float64> &torque, const Vec3<Float64> &position,
       const Vec3<Float64> &positionScaled,
       const Vec3<Float64> &positionUnwrapped, const Vec3<Int32> &imageID,
       const Vec3<Float64> &velocity, const Vec3<Float64> &force,
       const Vec3<Float64> &dipole);

  // Copy constructor
  Atom(const Atom &atom);

  // Move constructor
  Atom(const Atom &&atom) noexcept;

  ~Atom() = default;

 private:
  const Int32 atomID, molID, type;
  const Str element;

  const Float64 mass, charge;

  // Spherical particles
  const Float64 radius, diameter;

  // Angular velocity/momentum
  const Vec3<Float64> omega, angmom;

  // Torque on finite sized particles
  const Vec3<Float64> torque;

  // Atom coordinates
  const Vec3<Float64> position, positionScaled, positionUnwrapped;

  // Image ids
  const Vec3<Int32> imageID;

  // Atom velocities
  const Vec3<Float64> velocity;

  // Atom forces
  const Vec3<Float64> force;

  // Dipole
  const Vec3<Float64> dipole;
};

}  // namespace lmptools

#endif
