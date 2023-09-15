# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2023-09-15

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Dependencies

### CI/CD


## [2.11.0] - 2023-09-15

### Added
* Option to customize heading for GitHub Actions workflow job summary 

### Dependencies
* Bump cicirello/pyaction from 4.22.0 to 4.23.0


## [2.10.0] - 2023-09-04

### Added
* Option to suppress workflow job summary in GitHub Actions Mode (#126).

### Dependencies
* Bump cicirello/pyaction from 4.19.0 to 4.22.0


## [2.9.0] - 2023-05-24

### Added
* Support for glob patterns in GitHub Actions mode for specifying multiple JaCoCo reports for multi-module projects (note: CLI mode already supported this indirectly since the shell expands globs automatically).

### Dependencies
* Bump cicirello/pyaction from 4.11.1 to 4.19.0, including upgrading Python within the Docker container to 3.11.

### CI/CD
* Bump Python to 3.11 in CI/CD workflows.


## [2.8.1] - 2022-10-24

### Fixed
* The replacement for GitHub Action's deprecated `set-output` is not available yet for all self-hosted users. This patch
  handles that by using the new `$GITHUB_OUTPUT` environment file if it exists, and otherwise falling back to `set-output`.

### Dependencies
* Bump cicirello/pyaction from 4.11.0 to 4.11.1


## [2.8.0] - 2022-10-21

### Added
* Generate and output a GitHub Actions workflow job summary with the coverage percentages.

### Fixed
* Replaced use of GitHub Action's deprecated `set-output` workflow command.

### Dependencies
* Bump cicirello/pyaction from 4.6.0 to 4.11.0, which includes upgrading Python within the Docker container to 3.10.7.


## [2.7.0] - 2022-06-28

### Added
* CLI Mode: Ability to run as a command-line utility outside of GitHub Actions, such as part of a local build script, etc.

### Changed
* Refactored main control block to improve maintainability (#63).
* Refactored organization of source files (#64).
* Bumped base Docker image cicirello/pyaction from 4.1.0 to 4.6.0.

### CI/CD
* Added workflow to automatically publish CLI utility to PyPI on new releases of GitHub Action to GitHub Marketplace.


## [2.6.1] - 2022-02-18

### Fixed
* Suppressed Python's pycache on imports (fixes Issue #46).


## [2.6.0] - 2022-02-17

### Added
* Option to specify custom labels for the left side of the badges controlled
  by the new inputs `coverage-label` and `branches-label`.

### Changed
* Left-side text width and position calculated rather than hard-coded to
  width of "coverage" and "branches".
* Changed Dockerfile to pull base image from GitHub Container Registry, assuming
  within GitHub Actions likely faster to pull from GitHub rather than Docker Hub.
* Repository reorganized to move Python source code to a new src directory.


## [2.5.0] - 2021-11-11

### Added
* Option to generate a simple JSON summary report containing the coverage
  and branches coverage values as double-precision floating-point values.
  This may be useful as input to other tools. Additionally, if used in
  combination with the existing `fail-on-coverage-decrease` and/or 
  `fail-on-branches-decrease` features, those checks will be more accurate.
  This new feature is controlled by a pair of new inputs `generate-summary`
  and `summary-filename`. This feature is disabled by default.


## [2.4.1] - 2021-08-16

### Fixed
* Visual improvements to right side of badges:
  * Adjusted calculation of text lengths for right side of badges
    for improved character spacing.
  * Badge width now also adjusted by the right side text lengths.


## [2.4.0] - 2021-08-13

### Added
* Added an option to generate Shields.io JSON endpoints either in addition to, 
  or instead of, directly generating badges. For most users, the existing direct 
  generation of the badges is probably the preferred approach (e.g., probably 
  faster serving when loading README, and much simpler insertion of badge into 
  README). But for those who use one of Shields styles other than the default, 
  and who would like to be able to match the coverage badges to the style of 
  their project's other badges, then providing the ability to generate a 
  Shields JSON endpoint gives them the ability to do so. The new feature is 
  controlled by 4 new inputs: `generate-coverage-endpoint`, `generate-branches-endpoint`, 
  `coverage-endpoint-filename`, and `branches-endpoint-filename`. All of these 
  have default values and are optional. The current default behavior is retained, 
  so by default the JSON endpoints are not generated.


## [2.3.0] - 2021-6-25

### Added
* Customization of badge colors, using two new inputs (`colors` and 
  `intervals`). The defaults for the new inputs produce badges with
  the existing color scheme.


## [2.2.1] - 2021-5-20

### Changed
* Improved log messages related to the `fail-on-coverage-decrease` 
  and `fail-on-branches-decrease` inputs.
* Non-functional changes: Refactoring to improve maintainability.
* Use major release tag when pulling base docker image (e.g., automatically get non-breaking
  changes to base image, such as bug fixes, etc without need to update Dockerfile).
* Improved documentation of `fail-on-coverage-decrease` and `fail-if-coverage-less-than` inputs.


## [2.2.0] - 2021-5-8

### Added
* A new optional input, `fail-if-coverage-less-than`, that 
  enables failing the workflow run if coverage is below a 
  user specified minimum.
* A new optional input, `fail-if-branches-less-than`, that 
  enables failing the workflow run if branches coverage is below a 
  user specified minimum.
* A new optional input, `fail-on-coverage-decrease`, that enables 
  failing the workflow run if coverage decreased relative to previous run.
* A new optional input, `fail-on-branches-decrease`, that enables 
  failing the workflow run if branches coverage decreased relative to previous run.



## [2.1.2] - 2021-5-6

### CI/CD
* Introduced major release tag, and automated tag update upon release.


## [2.1.1] - 2021-5-5

### Fixed
* Previously, if any jacoco.csv files passed to the action were missing
  for any reason (e.g., typo in path or file name in workflow, or otherwise
  not generated by previous step of workflow), the action would simply fail
  resulting the the workflow run failing. Although in many cases this may be the
  desirable behavior, the action now logs the names of any missing jacoco
  report files to enable debugging what went wrong in a failed workflow run,
  and there is now an input, `on-missing-report`, that allows for specifying
  the behavior of the action in this case (e.g., user of the action can
  decide whether the workflow run should fail in this case).


## [2.1.0] - 2021-4-22

### Added
* Added support for multi-module projects: The `jacoco-badge-generator` is now
  able to generate coverage badges (both instructions and branches) for a multi-module
  project, computing the coverage percentages from a combination of the data
  from the separate coverage reports generated by JaCoCo for the sub-projects.

### Changed
* Updated example workflows to utilize the updated release of actions/setup-java.
* Bumped base docker image to pyaction-lite, v3.13.5.

### CI/CD
* Enabled CodeQL code scanning on all push/pull-request events.


## [2.0.1] - 2021-3-3

### Changed
* Changed the tag used to pull the base docker image from `latest`
  to the specific version number that is the latest. The reason for this change
  is to ensure that we have the opportunity to test against updates to
  the base image before such changes affect releases. Using the `latest`
  tag when pulling the base image runs the risk of a change in the base
  image breaking the action (although this risk is small).

### Fixed
* Fixed a bug related to permissions on the badges directory if it 
  didn't already exist prior to running the action. Bug only appeared to
  exhibit itself if the `jacoco-badge-generator` was used in combination with
  version 3.6 or later of the `peter-evans/create-pull-request` action, and only
  if the badges directory didn't already exist. This bug is now resolved.


## [2.0.0] - 2021-2-15

### Compatibility Notes
* If you are upgrading from an earlier version, and if 
  you were not using the `jacoco-badge-file` input (deprecated 
  since v1.2.0) to change the default location and name of the 
  badge file, then you can simply upgrade to v2.0.0 without need 
  to make any other changes to your workflow file.
* If you have been using the deprecated `jacoco-badge-file` input 
  to change the default location and name of the badge file, then 
  you will need to instead use the `badges-directory` and 
  the `coverage-badge-filename` inputs.

### Changed
* The documentation has been significantly revised to provide more 
  detail on the JaCoCo coverage metrics that are supported by 
  the jacoco-badge-generator.

### Removed
* Removed the previously deprecated input `jacoco-badge-file`.


## [1.2.1] - 2021-2-11

### Fixed
* Corrected division by zero error in the case when there are 
  either no instructions (e.g., running tests on an initially 
  empty class) or no branches (e.g., no if statements or switch 
  statements, etc). In such cases, badge generator will now 
  compute 100% coverage (e.g., if there aren't any instructions 
  to cover, your tests must have covered all 0 of the instructions).


## [1.2.0] - 2021-2-8

### Added
* Generation of a branches coverage badge (in addition to 
  the existing overall coverage badge).
* Inputs for finer grained control over the behavior of the 
  action (e.g., for controlling name and locations of generated 
  badges, as well as for controlling which badges are generated). 
  The default values for all of the new inputs are consistent 
  with the behavior of the previous release.

### Deprecated
* The `jacoco-badge-file` input is deprecated. In this release 
  it still functions as in prior releases, but it will be removed 
  in the next release. Users of the action should instead use the 
  combination of the new inputs `badges-directory` and 
  `coverage-badge-filename`. This change was made to simplify 
  configuration of badge file names now that the action generates 
  multiple badges.


## [1.1.0] - 2021-2-5

### Added
* An additional action output for the percentage of branches 
  covered. A future release will provide an option to generate 
  an additional badge for this.


## [1.0.0] - 2020-10-21

### Initial release
* The jacoco-badge-generator GitHub Action parses a `jacoco.csv` 
  from a Jacoco coverage report, computes the coverage percentage, 
  and generates a badge to provide an easy to read visual summary 
  of the code coverage of your test cases. The badge that is 
  generated is inspired by the style (including color palette) of 
  the badges of Shields.io, however, the badge is entirely 
  generated within the jacoco-badge-generator GitHub Action, 
  with no external calls.
