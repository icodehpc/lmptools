#pragma once

#include <stdint.h>
#include <array>
#include <numeric>
#include <cmath>
#include <concepts>

// To index into 3D arrays in a readable manner
enum class index: uint32_t {
    X,
    Y,
    Z,
};


// 3D vector class
template <typename T>
class Vec3 {
 public:
     Vec3() = default;
     Vec3(T x, T y, T z): _data(x, y, z) {}
     Vec3(const Vec3<T>& v): _data(v._data) {}

     T& operator[](uint8_t index) {
         return _data[index];
     }

     T norm() const {
         if constexpr(std::is_floating_point<T>) {
             // L2 norm
             return std::sqrt(std::inner_product(_data.begin(), _data.end(), _data.begin(), 0.0));
         } else if constexpr(std::is_integral<T>) {
             // L1 norm
             return std::abs(_data[0]) + std::abs(_data[1]) + std::abs(_data[2]);
         }
     }

 private:
     const std::array<T, 3> _data;
};

template <>
double Vec3<double>::norm() const {
    return std::sqrt(std::inner_product(_data.begin(), _data.end(), _data.begin(), 0.0));
}

template

enum class type_id : uint32_t {
  NONE,
  UINT32,
  UINT64,
  FLOAT32,
  FLOAT64,
  STRING
};
