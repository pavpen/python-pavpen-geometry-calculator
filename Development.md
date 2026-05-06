# Geometry Calculator Development Guide

## Development Environment

* Intall Python >= 3.12.
* Create a Python virtual environment with `hatch` installed.

  ```sh
  python -m pip install virtualenv
  python -m virtualenv py-venv/dev
  . py-venv/dev/Scripts/activate
  pip install hatch
  ```

* Install [git-cliff](https://git-cliff.org/)

  ```terminal
  cargo install git-cliff
  ```

## Type Checking

```terminal
hatch run types:check
```

## Testing

```terminal
hatch test
hatch run doc:test
```

## Check Test Coverage

```terminal
hatch test --cover
```

To view an HTML coverage report, after the command above, run:

```terminal
hatch run test-coverage:to_html
```

The report should be at
[tests/reports/coverage-html/index.html](tests/reports/coverage-html/index.html).

## Building Documentation

* See [doc/README.md](doc/README.md).
* Run:

  ```terminal
  hatch run doc:clean
  hatch run doc:build
  ```

## Building a Change Log

* Run `git-cliff`:

  ```terminal
  git-cliff
  ```

## Release Tagging

* After testing, and before packaging for release, tag the commit which
  corresponds to the code that's going to be released.
  * Use a `v` prefix, followed by a semantic version for the tag name.
  * Use an annotated Git tag for releases.
  * If you have a publicly known encryption key, preferably, also sign the
    release tag.  Otherwise, an unsigned tag is OK.
  * E.g.:

    ```terminal
    git tag --annotate v0.2.0
    ```

## Packaging

* Activate the Python development virtual environment from
  [§Development Environment](#development-environment).
* Run:

  ```terminal
  hatch build
  ```

## Package Publication

* Activate the Python development virtual environment from
  [§Development Environment](#development-environment).
* Run:

  ```terminal
  hatch publish
  ```
