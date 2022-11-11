#pragma once

#include "simulation.hpp"

#include "utils.hpp"

namespace lmptools {

SimulationBox::SimulationBox(double xlo, double xhi, double ylo, double yhi,
			     double zlo, double zhi)
    : xlo(xlo), xhi(xhi), ylo(ylo), yhi(yhi), zlo(zlo), zhi(zhi) {}

auto SimulationBox::operator==(const SimulationBox& other) {
  return is_equal(xlo, other.xlo, xhi, other.xhi, ylo, other.ylo, yhi,
		  other.yhi, zlo, other.zlo, zhi, other.zhi);
}

// Stdout simulation box
std::ostream& operator<<(std::ostream& out, const SimulationBox& box) {
  out << box.xlo << " " << box.xhi << "\n"
      << box.ylo << " " << box.yhi << "\n"
      << box.zlo << " " << box.zhi << "\n";
  return out;
}

// Triclinic box
TriclinicBox::TriclinicBox(double xlo, double xhi, double ylo, double yhi,
			   double zlo, double zhi, double xy, double xz,
			   double yz)
    : SimulationBox(xlo, xhi, ylo, yhi, zlo, zhi), xy(xy), xz(xz), yz(yz) {}

auto TriclinicBox::operator==(const TriclinicBox& other) {
  return is_equal(xlo, other.xlo, ylo, other.ylo, zlo, other.zlo, xhi,
		  other.xhi, yhi, other.yhi, zhi, other.zhi, xy, other.xy, xz,
		  other.xz, yz, other.yz);
}

// Stdout Triclinic box
std::ostream& operator<<(std::ostream& out, const TriclinicBox& box) {
  out << box.xlo << " " << box.xhi << " " << box.xy << "\n"
      << box.ylo << " " << box.yhi << " " << box.xz << "\n"
      << box.zlo << " " << box.zhi << " " << box.yz << "\n";
  return out;
}

}  // namespace lmptools
