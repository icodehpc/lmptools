#include "simulation.h"

#include "utils.h"

namespace lmptools {

SimulationBox::SimulationBox()
    : xlo{0.0}, xhi{0.0}, ylo{0.0}, yhi{0.0}, zlo{0.0}, zhi{0.0} {};

SimulationBox::SimulationBox(double xlo, double xhi, double ylo, double yhi,
                             double zlo, double zhi)
    : xlo(xlo), xhi(xhi), ylo(ylo), yhi(yhi), zlo(zlo), zhi(zhi) {}

bool SimulationBox::operator==(const SimulationBox &other) const noexcept {
  return is_equal(xlo, other.xlo, xhi, other.xhi, ylo, other.ylo, yhi,
                  other.yhi, zlo, other.zlo, zhi, other.zhi);
}

// Stdout simulation box
std::ostream &SimulationBox::operator<<(std::ostream &out) {
  out << xlo << " " << xhi << "\n"
      << ylo << " " << yhi << "\n"
      << zlo << " " << zhi << "\n";
  return out;
}

// Triclinic box
TriclinicBox::TriclinicBox(double xlo, double xhi, double ylo, double yhi,
                           double zlo, double zhi, double xy, double xz,
                           double yz)
    : SimulationBox(xlo, xhi, ylo, yhi, zlo, zhi), xy(xy), xz(xz), yz(yz) {}

bool TriclinicBox::operator==(const TriclinicBox &other) const noexcept {
  return is_equal(xlo, other.xlo, ylo, other.ylo, zlo, other.zlo, xhi,
                  other.xhi, yhi, other.yhi, zhi, other.zhi, xy, other.xy, xz,
                  other.xz, yz, other.yz);
}

// Stdout Triclinic box
std::ostream &TriclinicBox::operator<<(std::ostream &out) {
  out << xlo << " " << xhi << " " << xy << "\n"
      << ylo << " " << yhi << " " << xz << "\n"
      << zlo << " " << zhi << " " << yz << "\n";
  return out;
}

}  // namespace lmptools
