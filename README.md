# LMPTOOLS

![Tests](https://github.com/venkatbala/lmptools/actions/workflows/tests.yml/badge.svg)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/venkatBala/lmptools/develop.svg)](https://results.pre-commit.ci/latest/github/venkatBala/lmptools/develop)

**LMPTOOLS** is a Python package that aims to facilitate post-processing of [LAMMPS](https://www.lammps.org/) simulation data/dump files. The design of this tool
is modular in nature with the aim to be easily extensible. The design principle behind `lmptools` is that it treats the simulation outputs (dump files, log files) as a tape that
is read from start to end. As each entry in the dump file aka simulation snapshot is parsed from file, `lmptools` allows users to execute custom functions/code in order to allow post-processing.
