#ifndef SIMULATION_H
#define SIMULATION_H

#include <ostream>

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

  [[nodiscard]] auto lx() const -> double { return xhi - xlo; }
  [[nodiscard]] auto ly() const -> double { return yhi - ylo; }
  [[nodiscard]] auto lz() const -> double { return zhi - zlo; }

  // Comparison operator
  auto operator==(const SimulationBox &other);

  // ostream operator
  friend auto operator<<(std::ostream &out, const SimulationBox &box)
      -> std::ostream &;
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
  auto operator==(const TriclinicBox &other);

  // ostream operator
  friend auto operator<<(std::ostream &out, const TriclinicBox &box)
      -> std::ostream &;
};
}  // namespace lmptools

#endif
