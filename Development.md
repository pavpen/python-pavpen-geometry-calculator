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

## Packaging

* Activate the Python development virtual environment from
  [§Development Environment](#development-environment).
* Run:

  ```terminal
  hatch build
  ```

## Building Documentation

* See [doc/README.md](doc/README.md).
* Run:

  ```terminal
  hatch run doc:clean
  hatch run doc:build
  ```

## Package Publication

* Activate the Python development virtual environment from
  [§Development Environment](#development-environment).
* Run:

  ```terminal
  hatch publish
  ```
