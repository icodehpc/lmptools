#include "atom.h"

namespace lmptools {
Atom::Atom(Int32 atomID, Int32 molID, Int32 type, Str element, Float64 mass,
           Float64 charge, Float64 radius, Float64 diameter,
           const Vec3<Float64> &omega, const Vec3<Float64> &angmom,
           const Vec3<Float64> &torque, const Vec3<Float64> &position,
           const Vec3<Float64> &positionScaled,
           const Vec3<Float64> &positionUnwrapped, const Vec3<Int32> &imageID,
           const Vec3<Float64> &velocity, const Vec3<Float64> &force,
           const Vec3<Float64> &dipole)
    : atomID_{atomID},
      molID_{molID},
      type_{type},
      element_(std::move(element)),
      mass_{mass},
      charge_{charge},
      radius_{radius},
      diameter_{diameter},
      omega_{omega},
      angmom_{angmom},
      torque_{torque},
      position_{position},
      positionScaled_{positionScaled},
      positionUnwrapped_{positionUnwrapped},
      imageID_{imageID},
      velocity_{velocity},
      force_{force},
      dipole_{dipole} {}

Atom::Atom(const Atom &src)
    : atomID_(src.atomID_),
      molID_(src.molID_),
      type_(src.type_),
      mass_(src.mass_),
      charge_(src.charge_),
      radius_(src.radius_),
      diameter_(src.diameter_),
      omega_(src.omega_),
      angmom_(src.angmom_),
      torque_(src.torque_),
      position_(src.position_),
      positionScaled_(src.positionScaled_),
      positionUnwrapped_(src.positionUnwrapped_),
      imageID_(src.imageID_),
      velocity_(src.velocity_),
      force_(src.force_),
      dipole_(src.dipole_) {}

Atom &Atom::operator=(const Atom &src) {
  atomID_ = src.atomID_;
  molID_ = src.molID_;
  type_ = src.type_;
  element_ = src.element_;
  mass_ = src.mass_;
  charge_ = src.charge_;
  radius_ = src.radius_;
  diameter_ = src.diameter_;
  omega_ = src.omega_;
  angmom_ = src.angmom_;
  torque_ = src.torque_;
  position_ = src.position_;
  positionScaled_ = src.positionScaled_;
  positionUnwrapped_ = src.positionUnwrapped_;
  imageID_ = src.imageID_;
  velocity_ = src.velocity_;
  force_ = src.force_;
  dipole_ = src.dipole_;

  return *this;
}

}  // namespace lmptools
