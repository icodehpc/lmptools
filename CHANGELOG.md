# Changelog

## [Unreleased]

### Changed
- Seperated `CMakeLists.txt` for tests
- Updated default constructors for classes

### Added
- Added tests for `SimulationBox` and `utils`
- Added method to return a const reference to `Atom` from a snapshot

### Changed

- Implemented `DumpSnapshot` constructors in header itself
- Renamed unit test file
- Updated `operator<<` for `SimulationBox` and `TriclinicBox` to be class methods


## [0.20.8] - 2022-12-08
### Added
- Added `clang-format` check workflow

## [0.19.8] - 2022-12-08
### Changed
- Reverted adding prefix `pre` as the release is being tagged automatically as a pre-release

## [0.18.8] - 2022-12-08
### Fixed
- Update `refs` to `develop`
- added `develop` to the release branch when creating a release tag

## [0.18.7] - 2022-12-08
### Added
- Adding `DumpSnapshot` class skeleton

### Changed
- Update `tests.yml` to configure & build using CMake
- Use GoogleTest to run C++ tests
- Update CMakeLists.txt to build shared library with version information parsed from file

## [0.17.7] - 2022-11-11
### Added
- `C++` base type for `Atom` and `SimulationBox`
- Added `Vec3` template type for easy manipulation of 3-D vectors

### Fixed
- Updated `if` condition in `release` block in `tests.yml` workflow

## [0.16.6] - 2022-10-27
### Added
- Created base `Task` and `Pipeline` classes
- Added `append` method in `Pipeline` class to allow adding tasks as a list

## [0.15.6] - 2022-09-05
### Fixed
- fixed double quotes in step if condition in `tests.yml`
- fix step condition to only run for container `python:3.9-buster`

## [0.15.5] - 2022-09-05
### Added
- Adding `echo` statements for debugging

### Changed
- Updated `release` step in `tests.yml` workflow

## [0.14.5] - 2022-09-05
### Added
- Added abstract class for defining a `DumpFileParser`

### Changed
- Remove `push to main`

## [0.13.5] - 2022-08-27
### Changed
- Run `release` workflow from `develop` itself
- Remove `push to main` from tests.yml

## [0.12.5] - 2022-08-27
### Changed
- Updated `tests` and `release` workflow with logic to run from the `release` branch instead of main

## [0.11.5] - 2022-08-27
### Added
- Adding workflow step to add a changelog reminder to the PR

## [0.10.5] - 2022-08-27
### Changed
- default `continue_on_error` workflow option

## [0.9.5] - 2022-08-27
### Changed
- Updated `tests.yml` workflow by removing macos container

## [0.8.5] - 2022-08-27
### Added
- updating paths-ignored on which not to trigger changelog workflow
- add `if` guards around commit and update changelog steps

## [0.7.5] - 2022-08-27
### Added
- Added new worklow to enforce changelog updates

### Changed
- updated `changelog` workflow by removing the changelog check action

## [0.6.5] - 2022-08-27
### Changed
- changed the add and commit github action
- Trigger for `changelog` workflow

### Removed
- Updated the commit user name and email
- removed reference to github head ref

## [0.5.5] - 2022-08-27
### Changed
- Updated `changelog.yml` workflow to cleanup any temporary directories created

## 0.4.5 - 2022-08-27
### Added
- Add `CODEOWNERS` file
- Adding `changelog.yml` workflow to enable automatic versioning
- Added a hard check to force `CHANGELOG` to be updated as part of PRs
- Added `changelog` release step in `changelog.yml`
- Creating a PR with the changes to be merged into `develop`
- Adding merge PR action
- Adding PR approve action

### Changed
- Remove action to create PR with changes
- Merge changes into PR source
- Update `triggers` on `changelog` workflow
- Remove markdown ignore from ignored files
- Updated `README` by adding reference to CONTRIBUTING.md
- Updated `changelog` trigger to be `workflow_call`
- Fix PR merge action `pull_number` input
- Use `PULL_REQUEST_NUMBER` instead of step output

### Fixed
- Update changelog parsing logic
- Fixed `release changelog` block in `changelog.yml`
- Fixed `VERSION` interpolation in PR title

### Removed
- Removed `changelog_reminder` and `changelog_check` workflows
- cleanup empty dir

[Unreleased]: https://github.com/venkatBala/lmptools/changelog/compare/5aa33f400b8654304ed41aa1e208974d0bb9fd3b...develop
[0.20.8]: https://github.com/venkatBala/lmptools/changelog/compare/12bbc59693ec9c7fc0088ca1f93a6f500f39f4e2...develop
[0.19.8]: https://github.com/venkatBala/lmptools/changelog/compare/9566dd2f56a2b1b8601a6784fc01b76201eb95c4...develop
[0.18.8]: https://github.com/venkatBala/lmptools/changelog/compare/eda1c5029e831ddb9ad56e3a469ce2555f346fdd...develop
[0.18.7]: https://github.com/venkatBala/lmptools/changelog/compare/743d01b0409f6a602f7eaaf4c62e99c56c29b483...develop
[0.17.7]: https://github.com/venkatBala/lmptools/changelog/compare/e93f918164d616ad0112679194d6cee6bc886b08...develop
[0.16.6]: https://github.com/venkatBala/lmptools/changelog/compare/acd55682043e8ef5513712dbd7bb4e08f4162634...develop
[0.15.6]: https://github.com/venkatBala/lmptools/changelog/compare/85b0a03cc4c6c0bc4ccc978179ccc3bd0ba20ee4...develop
[0.15.5]: https://github.com/venkatBala/lmptools/changelog/compare/72428fad4c742a332e404abc8b65210137027760...develop
[0.14.5]: https://github.com/venkatBala/lmptools/changelog/compare/5bd6ed39675d545bb9665f29c2cf9622e1077d49...develop
[0.13.5]: https://github.com/venkatBala/lmptools/changelog/compare/e7cec797995cf0afbc839c072b64fdef7b0e6b01...develop
[0.12.5]: https://github.com/venkatBala/lmptools/changelog/compare/69512ae827611a030574edb1700fae3c5be7d70f...develop
[0.11.5]: https://github.com/venkatBala/lmptools/changelog/compare/f68bab2603b9424a8f61308dbfdc8f92520f40eb...develop
[0.10.5]: https://github.com/venkatBala/lmptools/changelog/compare/d2c7a576c3ebe81c6c6b0483e0cbf247ece979af...develop
[0.9.5]: https://github.com/venkatBala/lmptools/changelog/compare/e17f86f4f2ac71f2d98c14b19ce4713235fcd116...develop
[0.8.5]: https://github.com/venkatBala/lmptools/changelog/compare/1de7563d806d46a71b8d0c3be14a34035f9caa80...develop
[0.7.5]: https://github.com/venkatBala/lmptools/changelog/compare/34c410fb7c5a45a0c0e261953d76e0c1e9b5422d...develop
[0.6.5]: https://github.com/venkatBala/lmptools/changelog/compare/7e443f8160ac79d3ca85be1b93180e1c58848e02...develop
[0.5.5]: https://github.com/venkatBala/lmptools/changelog/compare/78ae5046d386cd6fed4492a8874e0a9da59ac1d0...develop
