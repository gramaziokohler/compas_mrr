# Changelog

<!-- markdownlint-disable-file MD024 -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.7] - 2021-08-25

### Changed
* Bumped max compas version to `<1.8`.

## [1.0.6] - 2021-03-18

### Changed
* Bumped max compas version to `1.2`.

## [1.0.5] - 2021-02-09

### Added

* Monkeypatch added for `compas._os.prepare_environment` applied if compas version
is less than `v0.19.2` to get around
[a bug affecting `compas.rpc.proxy`](https://github.com/compas-dev/compas/issues/701)

### Changed

* `MeasurementPoint` moved to its own module and made available as second level
import (`compas_mobile_robot_reloc.MeasurementPoint`). Still available from
`compas_mobile_robot_reloc.utils` for backwards compatibility.

## [1.0.4] - 2021-02-08

### Changed

* Dependency version specifier for compas' low bound set to `0.17.2`.

## [1.0.3] - 2021-02-01

### Changed

* Bumped compas to `<2.0`.

## [1.0.2] - 2021-01-04

No changes, version bumped to give give a clear indication of which conda
package to use. (Lingering package
[compas-mobile-robot-reloc](https://anaconda.org/conda-forge/compas-mobile-robot-reloc)
on conda forge.)

## [1.0.1] - 2020-12-18

### Added

* Moved MeasurementPoint from grasshopper document to `compas_mobile_robot_reloc.utils`.

## [1.0.0] - 2020-12-18

Package broken out from
[rapid_clay_formations_fab](https://github.com/gramaziokohler/rapid_clay_formations_fab).

Typing and tests added.
