# Changelog

## [Unreleased]

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

[Unreleased]: https://github.com/venkatBala/lmptools/changelog/compare/78ae5046d386cd6fed4492a8874e0a9da59ac1d0...develop
