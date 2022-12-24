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
  Atom(const Atom &&atom) noexcept {}

  ~Atom() = default;

  // Assignment operator
  Atom &operator=(const Atom &src);

 private:
  Int32 atomID_, molID_, type_;
  Str element_;

  Float64 mass_, charge_;

  // Spherical particles
  Float64 radius_, diameter_;

  // Angular velocity/momentum
  Vec3<Float64> omega_, angmom_;

  // Torque on finite sized particles
  Vec3<Float64> torque_;

  // Atom coordinates
  Vec3<Float64> position_, positionScaled_, positionUnwrapped_;

  // Image ids
  Vec3<Int32> imageID_;

  // Atom velocities
  Vec3<Float64> velocity_;

  // Atom forces
  Vec3<Float64> force_;

  // Dipole
  Vec3<Float64> dipole_;
};

}  // namespace lmptools

#endif
