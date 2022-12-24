#include "atom.h"

#include "utils.h"

namespace lmptools {
Atom::Atom(Int32 id, Int32 mol_id, Int32 type, Str element, Float64 mass,
           Float64 charge, Float64 radius, Float64 diameter,
           const Vec3<Float64> &omega, const Vec3<Float64> &angmom,
           const Vec3<Float64> &torque, const Vec3<Float64> &position,
           const Vec3<Float64> &position_scaled,
           const Vec3<Float64> &position_unwrapped, const Vec3<Int32> &image_id,
           const Vec3<Float64> &velocity, const Vec3<Float64> &force,
           const Vec3<Float64> &dipole)
    : id{id},
      mol_id{mol_id},
      type{type},
      element(std::move(element)),
      mass{mass},
      charge{charge},
      radius{radius},
      diameter{diameter},
      omega{omega},
      angmom{angmom},
      torque{torque},
      position{position},
      position_scaled{position_scaled},
      position_unwrapped{position_unwrapped},
      image_id{image_id},
      velocity{velocity},
      force{force},
      dipole{dipole} {}

Atom::Atom(const Atom &src)
    : id(src.id),
      mol_id(src.mol_id),
      type(src.type),
      mass(src.mass),
      charge(src.charge),
      radius(src.radius),
      diameter(src.diameter),
      omega(src.omega),
      angmom(src.angmom),
      torque(src.torque),
      position(src.position),
      position_scaled(src.position_scaled),
      position_unwrapped(src.position_unwrapped),
      image_id(src.image_id),
      velocity(src.velocity),
      force(src.force),
      dipole(src.dipole) {}

Atom &Atom::operator=(const Atom &src) noexcept {
  id = src.id;
  mol_id = src.mol_id;
  type = src.type;
  element = src.element;
  mass = src.mass;
  charge = src.charge;
  radius = src.radius;
  diameter = src.diameter;
  omega = src.omega;
  angmom = src.angmom;
  torque = src.torque;
  position = src.position;
  position_scaled = src.position_scaled;
  position_unwrapped = src.position_unwrapped;
  image_id = src.image_id;
  velocity = src.velocity;
  force = src.force;
  dipole = src.dipole;

  return *this;
}

bool Atom::operator==(const Atom &other) const noexcept {
  return is_equal(id, other.id, mol_id, other.mol_id, type, other.type, element,
                  other.element, mass, other.mass, charge, other.charge, radius,
                  other.radius, diameter, other.diameter, omega, other.omega,
                  angmom, other.angmom, torque, other.torque, position,
                  other.position, position_scaled, other.position_scaled,
                  position_unwrapped, other.position_unwrapped, image_id,
                  other.image_id, velocity, other.velocity, force, other.force,
                  dipole, other.dipole);
}

}  // namespace lmptools
