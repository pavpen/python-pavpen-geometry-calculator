# Geometry Calculator Documentation Source

* The [`source/`](source/) directory contains the definitions for generating
  project user documentation.
* Generated user documentation is output under [`build/`](build/).
* Developer documentation for maintaining this repository (such as this very
  `README.md`) can be added under a `develope/` directory, if necessary.

## Building User Documentation

* Use `cd .. && hatch run doc:build`.
* You can activate the necessary Python virtual environment, then execute
  [Sphinx commands](https://www.sphinx-doc.org/en/master/usage/quickstart.html#running-the-build),
  such as another builder, for custom documentation builds.
  * E.g., to build the default HTML documentation:

    ```terminal
    make html
    ```

  * Output should be accessible from
    [build/html/index.html](build/html/index.html).

## Running DocTests in the Documentation

* Use `cd .. && hatch run doc:test`.
* This runs `sphinx-build -M doctest doc/source doc/build`.
