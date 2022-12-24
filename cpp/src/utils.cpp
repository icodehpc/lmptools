#include "utils.h"

template <typename T>
bool operator==(const lmptools::Vec3<T>& a,
                const lmptools::Vec3<T>& b) noexcept {
  return lmptools::is_equal(a[0], b[0], a[1], b[1], a[2], b[2]);
}

template <typename T>
T lmptools::Vec3<T>::norm() const {
  if constexpr (std::is_floating_point<T>::value) {
    // L2 norm
    return std::sqrt(
        std::inner_product(data_.begin(), data_.end(), data_.begin(), 0.0));
  } else if constexpr (std::is_integral<T>::value) {
    // L1 norm
    return std::abs(data_[0]) + std::abs(data_[1]) + std::abs(data_[2]);
  }
}

template <typename T>
lmptools::Vec3<T>& lmptools::Vec3<T>::operator=(const lmptools::Vec3<T>& src) {
  data_[0] = src[0];
  data_[1] = src[1];
  data_[2] = src[2];
  return *this;
}
