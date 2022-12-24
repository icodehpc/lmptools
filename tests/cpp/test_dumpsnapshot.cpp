#include <gtest/gtest.h>

#include <vector>

#include "atom.h"
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

TEST(DumpSnapshot, DumpStyleTimestepConstructor) {
  lmptools::DumpSnapshot snapshot(0, 0);

  ASSERT_EQ(snapshot.dumpStyle(), 0);
  ASSERT_EQ(snapshot.timestep(), 0);
}

TEST(DumpSnapshot, DumpStyleTimestepNatomsBoxConstructor) {
  lmptools::DumpSnapshot snapshot(0, 0, 0, lmptools::SimulationBox());

  ASSERT_EQ(snapshot.dumpStyle(), 0);
  ASSERT_EQ(snapshot.timestep(), 0);
  ASSERT_EQ(snapshot.natoms(), 0);
  ASSERT_EQ(snapshot.box(), lmptools::SimulationBox());
}

TEST(DumpSnapshot, FullConstructor) {
  std::vector<lmptools::Atom> atoms;
  lmptools::DumpSnapshot snapshot(0, 0, 0, lmptools::SimulationBox(), atoms);

  ASSERT_EQ(snapshot.dumpStyle(), 0);
  ASSERT_EQ(snapshot.timestep(), 0);
  ASSERT_EQ(snapshot.natoms(), 0);
  ASSERT_EQ(snapshot.box(), lmptools::SimulationBox());
}
