#include "../include/atom.hpp"


lmptools::Atom::Atom(uint32_t id, uint32_t mol, uint32_t type, const std::string& element,
            double mass, double charge, double radius, double diameter,
            const Vec3<double>& omega, const Vec3<double>& angmom,
            const Vec3<double>& torque, const Vec3<double>& x, const Vec3<double>& xs,
            const Vec3<double>& xu, const Vec3<uint32_t>& imageId, const Vec3<double>& v,
            const Vec3<double>& f, const Vec3<double>& mu): id{id}, mol{mol}, type{type}, element{element},
                mass{mass}, charge{charge}, radius{radius}, diameter{diameter},
                omega{omega}, angmom{angmom}, torque{torque}, x{x}, xs{xs}, xu{xu},
                imageId{imageId}, v{v}, f{f}, mu{mu} {}
