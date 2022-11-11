#pragma once

#include <stdint.h>

#include <array>
#include <cmath>
#include <concepts>
#include <numeric>

namespace lmptools {

template <typename T>
concept IsEqualityComparable = std::equality_comparable<T>;

// Check equality between an even number of arbitrary arguments of the same type
template <IsEqualityComparable T>
auto is_equal(T a, T b) {
  return a == b;
}

template <IsEqualityComparable T, IsEqualityComparable... Args>
auto is_equal(T a, T b, Args... args) {
  return is_equal(a, b) && is_equal(args...);
}

// To index into 3D arrays in a readable manner
enum class index : uint32_t {
  X,
  Y,
  Z,
};

// 3D vector class
template <typename T>
class Vec3 {
 public:
  explicit Vec3(T x) : Vec3(x, x, x) {}
  Vec3(T x, T y, T z) : _data(x, y, z) {}
  Vec3(const Vec3<T>& v) : _data(v._data) {}

  T& operator[](uint8_t index) const { return _data[index]; }

  T norm() const {
    if constexpr (std::is_floating_point<T>::value) {
      // L2 norm
      return std::sqrt(
	  std::inner_product(_data.begin(), _data.end(), _data.begin(), 0.0));
    } else if constexpr (std::is_integral<T>::value) {
      // L1 norm
      return std::abs(_data[0]) + std::abs(_data[1]) + std::abs(_data[2]);
    }
  }

 private:
  const std::array<T, 3> _data;
};

enum class type_id : uint32_t {
  NONE,
  UINT32,
  UINT64,
  FLOAT32,
  FLOAT64,
  STRING
};

}  // namespace lmptools
