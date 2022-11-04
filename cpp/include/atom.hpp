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

     double mass, charge;

     // Unscaled atom coordinates
     vec3<double> x;
     
     // scaled atom coordinates
     vec3<double> xs;

     // unwrapped atom coordinates
     vec3<double> xu;

     // image id
     vec3<uint32_t> imageId;

     // Atom velocities
     vec3<double> v;

     // Atom forces
     vec3<double> f;

     // Dipole
     vec3<double> mu;

};
