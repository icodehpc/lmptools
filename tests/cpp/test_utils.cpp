#include "gtest/gtest.h"
#include "utils.h"

TEST(UTILS, TestVec3Constructor) {
  lmptools::Vec3<double> v;

  EXPECT_DOUBLE_EQ(v[0], 0.0);
  EXPECT_DOUBLE_EQ(v[1], 0.0);
  EXPECT_DOUBLE_EQ(v[2], 0.0);
}
