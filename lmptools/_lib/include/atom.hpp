#pragma once

#include <string>

#include "utils.hpp"

namespace lmptools {

/*
 * Base atom class based on the LAMMPS atom style
 *
 * */
class Atom {
 public:
  Atom() = delete;
  Atom(uint32_t id, uint32_t mol, uint32_t type, const std::string& element,
       double mass, double charge, double radius, double diameter,
       const Vec3<double>& omega, const Vec3<double>& angmom,
       const Vec3<double>& torque, const Vec3<double>& x,
       const Vec3<double>& xs, const Vec3<double>& xu,
       const Vec3<uint32_t>& imageId, const Vec3<double>& v,
       const Vec3<double>& f, const Vec3<double>& mu);
  ~Atom() = default;

  const int id, mol, type;
  const std::string element;

  const double mass, charge;

  // Spherical particles
  const double radius, diameter;

  // Angular velocity/momentum
  const Vec3<double> omega, angmom;

  // Torque on finite sized particles
  const Vec3<double> torque;

  // Unscaled atom coordinates
  const Vec3<double> x;

  // Scaled atom coordinates
  const Vec3<double> xs;

  // Unwrapped atom coordinates
  const Vec3<double> xu;

  // Image ids
  const Vec3<uint32_t> imageId;

  // Atom velocities
  const Vec3<double> v;

  // Atom forces
  const Vec3<double> f;

  // Dipole
  const Vec3<double> mu;
};

}  // namespace lmptools
