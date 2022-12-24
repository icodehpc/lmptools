#include "gtest/gtest.h"
#include "simulation.h"

TEST(SimulationBox, DefaultConstruction) {
  lmptools::SimulationBox box;

  ASSERT_EQ(box.xlo, 0.0);
  ASSERT_EQ(box.xhi, 0.0);
  ASSERT_EQ(box.ylo, 0.0);
  ASSERT_EQ(box.yhi, 0.0);
  ASSERT_EQ(box.zlo, 0.0);
  ASSERT_EQ(box.zhi, 0.0);
}

TEST(SimulationxBox, SimpleConstructor) {
  lmptools::SimulationBox box(0.0, 1.0, 0.0, 1.0, 0.0, 1.0);

  ASSERT_EQ(box.xlo, 0.0);
  ASSERT_EQ(box.xhi, 1.0);
  ASSERT_EQ(box.ylo, 0.0);
  ASSERT_EQ(box.yhi, 1.0);
  ASSERT_EQ(box.zlo, 0.0);
  ASSERT_EQ(box.zhi, 1.0);
}
