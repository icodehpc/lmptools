#include <gtest/gtest.h>

#include "dump.h"
#include "simulation.h"

TEST(Pass, Always) { EXPECT_EQ(1, 1); }

TEST(DumpSnapshot, DefaultConstructor) {
  lmptools::DumpSnapshot snapshot;

  ASSERT_EQ(snapshot.dumpStyle(), 0);
  ASSERT_EQ(snapshot.timestep(), 0);
  ASSERT_EQ(snapshot.natoms(), 0);
  ASSERT_EQ(snapshot.box(), lmptools::SimulationBox());
}
