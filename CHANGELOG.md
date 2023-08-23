# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [1.0.1](https://github.com/maxb2/typer-config/releases/tag/1.0.1) - 2023-08-23

<small>[Compare with 1.0.0](https://github.com/maxb2/typer-config/compare/1.0.0...1.0.1)</small>

### Bug Fixes

- add py.typed so mypy will use our annotations ([ac56f1c](https://github.com/maxb2/typer-config/commit/ac56f1c02f5e549cd1713f4eb3c7d147a139b5ab) by Matt Anderson).

## [1.0.0](https://github.com/maxb2/typer-config/releases/tag/1.0.0) - 2023-07-19

<small>[Compare with 0.6.1](https://github.com/maxb2/typer-config/compare/0.6.1...1.0.0)</small>

### Breaking Changes

- remove deprecated code (#45) ([e363a80](https://github.com/maxb2/typer-config/commit/e363a80a510abccbe6538acf50ca43a755f710bd) by Matthew Anderson).

### Code Refactoring

- ruff linting (#44) ([a79245a](https://github.com/maxb2/typer-config/commit/a79245a0c8e02513c62437bf56d117b910f9a1a5) by Matthew Anderson).

## [0.6.1](https://github.com/maxb2/typer-config/releases/tag/0.6.1) - 2023-07-17

<small>[Compare with 0.6.0](https://github.com/maxb2/typer-config/compare/0.6.0...0.6.1)</small>

- update docs to use `Annotated` parameters (#41) ([f2a8a25](https://github.com/maxb2/typer-config/commit/f2a8a254d971d064f66d7c02bed9bf4c22b64c24) by Matthew Anderson).

## [0.6.0](https://github.com/maxb2/typer-config/releases/tag/0.6.0) - 2023-07-17

<small>[Compare with 0.5.0](https://github.com/maxb2/typer-config/compare/0.5.0...0.6.0)</small>

### Features

- dump configuration on invocation (#27) ([b2c7b42](https://github.com/maxb2/typer-config/commit/b2c7b423d2cfc334cc9264544ed62256734acf7a) by Matthew Anderson).
- config decorator (#34) ([ae8e44d](https://github.com/maxb2/typer-config/commit/ae8e44df68c0ccf24be42af598050278f1d79737) by Matthew Anderson).

## [0.5.0](https://github.com/maxb2/typer-config/releases/tag/0.5.0) - 2023-05-25

<small>[Compare with 0.4.0](https://github.com/maxb2/typer-config/compare/0.4.0...0.5.0)</small>

### Features

- loader conditionals (#23) ([4bb82de](https://github.com/maxb2/typer-config/commit/4bb82de3a9d1e355a0eb0048d10d4246d57a5c22) by Matthew Anderson).

## [0.4.0](https://github.com/maxb2/typer-config/releases/tag/0.4.0) - 2023-05-22

<small>[Compare with 0.3.0](https://github.com/maxb2/typer-config/compare/0.3.0...0.4.0)</small>

### Features

- config loader transformer (#21) ([7af9695](https://github.com/maxb2/typer-config/commit/7af96956b7e1e0170cd5a8a0d7c5076f76f53aa0) by Matthew Anderson). * deps: update to fixed version of griffe

## [0.3.0](https://github.com/maxb2/typer-config/releases/tag/0.3.0) - 2023-05-17

<small>[Compare with 0.2.0](https://github.com/maxb2/typer-config/compare/0.2.0...0.3.0)</small>

### Features

- INI support (#17) ([2ec9aa5](https://github.com/maxb2/typer-config/commit/2ec9aa5dbacb5d4f08ccaffb0b2d80d492355fef) by Matthew Anderson).

### Code Refactoring

- reorder release steps ([6f83ed0](https://github.com/maxb2/typer-config/commit/6f83ed0192447fb2c477d31f6006c1ce71b6da25) by Matthew Anderson).

## [0.2.0](https://github.com/maxb2/typer-config/releases/tag/0.2.0) - 2023-05-17

<small>[Compare with 0.1.3](https://github.com/maxb2/typer-config/compare/0.1.3...0.2.0)</small>

### Features

- dotenv (#15) ([28f5e61](https://github.com/maxb2/typer-config/commit/28f5e611a9885693ac3c7c156095b5f6fd3ac7e7) by Matthew Anderson). * feat: dotenv support

### Bug Fixes

- tooling ([ae24220](https://github.com/maxb2/typer-config/commit/ae242202635cc02e1a4aa7e7258ee2e78886c22b) by Matthew Anderson).

## [0.1.3](https://github.com/maxb2/typer-config/releases/tag/0.1.3) - 2023-05-15

<small>[Compare with 0.1.2](https://github.com/maxb2/typer-config/compare/0.1.2...0.1.3)</small>

### Features

- add test for pyproject example (#5) ([dbbd1b6](https://github.com/maxb2/typer-config/commit/dbbd1b6fcb0154b8455309fb642543a4d12b4c6a) by Matthew Anderson).

### Bug Fixes

- change local type module name to match typer ([0c087ff](https://github.com/maxb2/typer-config/commit/0c087ff29922215ba2d5060b9e19f54b5450dfdb) by Matthew Anderson).
- typo ([b7a10c3](https://github.com/maxb2/typer-config/commit/b7a10c3bd035974153a94d0bdd2dd64a9f76fe18) by Matthew Anderson).

## [0.1.2](https://github.com/maxb2/typer-config/releases/tag/0.1.2) - 2023-05-01

<small>[Compare with first commit](https://github.com/maxb2/typer-config/compare/04821fd8f76abb5309e10d2602227d05098d86e3...0.1.2)</small>

### Features

- simple example as test ([d59962e](https://github.com/maxb2/typer-config/commit/d59962e24cdbe50db6eb632bbb5ca49922955639) by Matthew Anderson).
- initial features ([4298289](https://github.com/maxb2/typer-config/commit/4298289ac4ff041e5481d837f3ab38a00f052707) by Matthew Anderson).

### Bug Fixes

- linter ([8bfeb82](https://github.com/maxb2/typer-config/commit/8bfeb822906302c1021d5979404ed644284a87be) by Matthew Anderson).
- tomllib ([15f53a5](https://github.com/maxb2/typer-config/commit/15f53a5c6d9a90d99a7c17f020269177bd799ac3) by Matthew Anderson).
- typer BadParameter ([64868a3](https://github.com/maxb2/typer-config/commit/64868a33a6bb6a5833c40a02c6e2771b10a16cbc) by Matthew Anderson).
