#include <gtest/gtest.h>

#include "atom.h"
#include "dump.h"
#include "simulation.h"

TEST(Pass, Always) { EXPECT_EQ(1, 1); }

TEST(DumpSnapshot, Getters) {
  lmptools::SimulationBox box;
  box.xlo = 0.0;
  const lmptools::DumpSnapshot snapshot(1, 100, 100, box);
  ASSERT_EQ(snapshot.dumpStyle(), 1);
  ASSERT_EQ(snapshot.timestep(), 100ul);
  ASSERT_EQ(snapshot.natoms(), 100);
  ASSERT_EQ(snapshot.box(), box);
}

TEST(DumpSnapshot, Setters) {
  lmptools::DumpSnapshot snapshot;

  snapshot.dumpStyle() = 1;
  snapshot.timestep() = 100;
  snapshot.box() = lmptools::SimulationBox();

  ASSERT_EQ(snapshot.dumpStyle(), 1);
  ASSERT_EQ(snapshot.timestep(), 100);
  ASSERT_EQ(snapshot.box(), lmptools::SimulationBox());
}

TEST(DumpSnapshot, DefaultConstructor) { lmptools::DumpSnapshot snapshot; }
