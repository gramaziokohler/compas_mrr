# Changelog

<!-- markdownlint-disable-file MD024 -->

## 2021-03-18 - 1.0.6

### Changed
* Bumped max compas version to `1.2`.

## 2021-02-09 - 1.0.5

### Added

* Monkeypatch added for `compas._os.prepare_environment` applied if compas version
is less than `v0.19.2` to get around
[a bug affecting `compas.rpc.proxy`](https://github.com/compas-dev/compas/issues/701)

### Changed

* `MeasurementPoint` moved to its own module and made available as second level
import (`compas_mobile_robot_reloc.MeasurementPoint`). Still available from
`compas_mobile_robot_reloc.utils` for backwards compatibility.

## 2021-02-08 - 1.0.4

### Changed

* Dependency version specifier for compas' low bound set to `0.17.2`.

## 2021-02-01 - 1.0.3

### Changed

* Bumped compas to `<2.0`.

## 2021-01-04 - 1.0.2

No changes, version bumped to give give a clear indication of which conda
package to use. (Lingering package
[compas-mobile-robot-reloc](https://anaconda.org/conda-forge/compas-mobile-robot-reloc)
on conda forge.)

## 2020-12-18 - 1.0.1

### Added

* Moved MeasurementPoint from grasshopper document to `compas_mobile_robot_reloc.utils`.

## 2020-12-18 - 1.0.0

Package broken out from
[rapid_clay_formations_fab](https://github.com/gramaziokohler/rapid_clay_formations_fab).

Typing and tests added.
