#ifndef SIMULATION_H
#define SIMULATION_H

#include <ostream>

namespace lmptools {
struct SimulationBox {
  double xlo;
  double xhi;
  double ylo;
  double yhi;
  double zlo;
  double zhi;

  SimulationBox()
      : xlo{0.0}, xhi{0.0}, ylo{0.0}, yhi{0.0}, zlo{0.0}, zhi{0.0} {};
  SimulationBox(double xlo, double xhi, double ylo, double yhi, double zlo,
                double zhi);

  ~SimulationBox() = default;

  [[nodiscard]] auto lx() const noexcept { return xhi - xlo; }
  [[nodiscard]] auto ly() const noexcept { return yhi - ylo; }
  [[nodiscard]] auto lz() const noexcept { return zhi - zlo; }

  // Comparison operator
  bool operator==(const SimulationBox &other) const noexcept;
  // auto operator==(const SimulationBox &other);

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
  bool operator==(const TriclinicBox &other) const noexcept;
  //  auto operator==(const TriclinicBox &other);

  // ostream operator
  std::ostream &operator<<(std::ostream &out);
};
}  // namespace lmptools

#endif
