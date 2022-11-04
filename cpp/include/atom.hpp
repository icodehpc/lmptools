#pragma once


#include <string>
#include "types.hpp"

/*
 * Base atom class based on the LAMMPS atom style
 *
 * */
class Atom {
 public:
     const int id, mol, type;
     const std::string element;

     const double mass, charge;

     // Spherical particles
     const double radius, diameter;

     // Angular velocity/momentum
     const Vec3<double> omega, angmom;

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
