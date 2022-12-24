#ifndef UTILS_H_
#define UTILS_H_

#include <array>
#include <cmath>
#include <concepts>
#include <cstdint>
#include <numeric>
#include <string>

namespace lmptools {

using Int32 = uint32_t;
using Int64 = uint64_t;
using Float32 = float;
using Float64 = double;
using Str = std::string;

template <typename T>
concept IsEqualityComparable = std::equality_comparable<T>;

// Check equality between an even number of arbitrary arguments of the same
// type
template <IsEqualityComparable T>
auto is_equal(T first, T second) {
  return first == second;
}

template <IsEqualityComparable T, IsEqualityComparable... Args>
auto is_equal(T first, T second, Args... args) {
  return is_equal(first, second) && is_equal(args...);
}

// To index into 3D arrays in a readable manner
enum class index : Int32 {
  X,
  Y,
  Z,
};

// 3D vector class
template <typename T>
class Vec3 {
 public:
  Vec3() : data_{} {}
  explicit Vec3(T x) : Vec3(x, x, x) {}
  Vec3(T x, T y, T z) : data_(x, y, z) {}
  Vec3(const Vec3<T>& v) : data_(v.data_) {}

  const T& operator[](Int32 index) const { return data_[index]; }
  T& operator[](Int32 index) { return data_[index]; }

  T norm() const;

  Vec3& operator=(const Vec3& src);

  friend bool operator==(const Vec3& a, const Vec3& b) noexcept;

 private:
  std::array<T, 3> data_;
};

}  // namespace lmptools

#endif
