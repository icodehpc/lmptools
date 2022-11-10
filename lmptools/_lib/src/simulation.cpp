#pragma once

#include "simulation.hpp"

namespace lmptools {
SimulationBox::SimulationBox(double xlo, double xhi,
														 double ylo, double yhi,
														double zlo, double zhi,
							 							double xy, double xz, double yz,
							 							bool triclinic): xlo(xlo), xhi(xhi), ylo(ylo), yhi(yhi),
														zlo(zlo), zhi(zhi), xy(xy), xz(xz), yz(yz), triclinic(triclinic) {}


bool SimulationBox::operator==(const SimulationBox& other) {
	auto is_xlo_equal = (xlo == other.xlo);
	auto is_xhi_equal = (xhi == other.xhi);
	auto is_ylo_equal = (ylo == other.ylo);
	auto is_yhi_equal = (yhi == other.yhi);
	auto is_zlo_equal = (zlo == other.zlo);
	auto is_zhi_equal = (zhi == other.zhi);
	auto is_xz_equal = (xz == other.xz);
	auto is_xy_equal = (xy == other.xy);
	auto is_yz_equal = (yz == other.yz);
	auto is_triclinic_equal = (triclinic == other.triclinic);

	return (is_xlo_equal && is_xhi_equal) && \
		(is_ylo_equal && is_yhi_equal) && \
		(is_zlo_equal && is_zhi_equal) && \
		(is_xz_equal && is_xy_equal && is_yz_equal) && is_triclinic_equal;

}

// Stdout simulation box
std::ostream& operator<<(std::ostream& out, const SimulationBox& box) {
	out << box.xlo << " " << box.xhi << " " << box.xy << "\n" \
		<< box.ylo << " " << box.yhi << " " << box.yz << "\n" \
		<< box.zlo << " " << box.zhi << " " << box.xz << "\n";
	return out;
}



}
