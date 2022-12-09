#ifndef SIMULATION_H
#define SIMULATION_H

#include <ostream>

namespace lmptools {
class SimulationBox {
 public:
  double xlo, xhi;
  double ylo, yhi;
  double zlo, zhi;

  SimulationBox() = default;
  SimulationBox(double xlo, double xhi, double ylo, double yhi, double zlo,
                double zhi);

  ~SimulationBox() = default;

  [[nodiscard]] auto lx() const -> double { return xhi - xlo; }
  [[nodiscard]] auto ly() const -> double { return yhi - ylo; }
  [[nodiscard]] auto lz() const -> double { return zhi - zlo; }

  // Comparison operator
  bool operator==(const SimulationBox &other) const = default;
  auto operator==(const SimulationBox &other);

  // ostream operator
  std::ostream &operator<<(std::ostream &out);
};

// Triclinic box
class TriclinicBox : public SimulationBox {
 public:
  TriclinicBox() = default;
  ~TriclinicBox();
  double xy, xz, yz;
  TriclinicBox(double xlo, double xhi, double ylo, double yhi, double zlo,
               double zhi, double xy, double xz, double yz);

  // Comparison operator
  bool operator==(const TriclinicBox &other) const = default;
  auto operator==(const TriclinicBox &other);

  // ostream operator
  std::ostream &operator<<(std::ostream &out);
};
}  // namespace lmptools

#endif
