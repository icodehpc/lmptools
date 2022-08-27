# Changelog

## [Unreleased]

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

[Unreleased]: https://github.com/venkatBala/lmptools/changelog/compare/1de7563d806d46a71b8d0c3be14a34035f9caa80...develop
[0.7.5]: https://github.com/venkatBala/lmptools/changelog/compare/34c410fb7c5a45a0c0e261953d76e0c1e9b5422d...develop
[0.6.5]: https://github.com/venkatBala/lmptools/changelog/compare/7e443f8160ac79d3ca85be1b93180e1c58848e02...develop
[0.5.5]: https://github.com/venkatBala/lmptools/changelog/compare/78ae5046d386cd6fed4492a8874e0a9da59ac1d0...develop
