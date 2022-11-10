#pragma once

#include <iostream>

namespace lmptools {
class SimulationBox {
 public:
	 double xlo, xhi;
	 double ylo, yhi;
	 double zlo, zhi;
	 double xy, xz, yz = 0.0;
	 bool triclinic = false;

	 SimulationBox() = delete;
	 SimulationBox(double xlo, double xhi,
			 double ylo, double yhi,
			 double zlo, double zhi,
			 double xy, double xz, double yz,
			 bool triclinic);

	 ~SimulationBox() = default;

	 double lx() const { return xhi - xlo; }
	 double ly() const { return yhi - ylo; }
	 double lz() const { return zhi - zlo; }

	 // Comparison operator
	 bool operator==(const SimulationBox& other);

	 // ostream operator
	 friend std::ostream& operator<<(std::ostream& out, const SimulationBox& box);

};
}
