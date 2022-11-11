#pragma once

#include <iostream>

namespace lmptools {
class SimulationBox {
 public:
  double xlo, xhi;
  double ylo, yhi;
  double zlo, zhi;

  SimulationBox() = delete;
  SimulationBox(double xlo, double xhi, double ylo, double yhi, double zlo,
		double zhi);

  ~SimulationBox() = default;

  double lx() const { return xhi - xlo; }
  double ly() const { return yhi - ylo; }
  double lz() const { return zhi - zlo; }

  // Comparison operator
  auto operator==(const SimulationBox& other);

  // ostream operator
  friend std::ostream& operator<<(std::ostream& out, const SimulationBox& box);
};

// Triclinic box
class TriclinicBox : public SimulationBox {
 public:
  double xz, xy, yz;
  TriclinicBox(double xlo, double xhi, double ylo, double yhi, double zlo,
	       double zhi, double xy, double xz, double yz);

  TriclinicBox() = delete;
  ~TriclinicBox();

  // Comparison operator
  auto operator==(const TriclinicBox& other);

  // ostream operator
  friend std::ostream& operator<<(std::ostream& out, const TriclinicBox& box);
};
}  // namespace lmptools
