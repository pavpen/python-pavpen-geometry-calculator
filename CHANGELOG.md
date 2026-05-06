# Changelog

## [unreleased]

### 🐛 Bug Fixes

- Import failure due to missing `_version.py` in source, and wheel packages

### 💼 Other

- Add Change Log generation with `git-cliff`

## [0.2.0] - 2026-05-06

### 🚀 Features

- [**breaking**] Rename `VectorFieldFloatOperations` to `FloatVectorFieldOperations`
- [**breaking**] Rename `TupleVectorFieldFloatOperations` to `TupleFloatVectorFieldOperations`
- [**breaking**] Raise an exception from each abstract method that must be overridden
- [**breaking**] Rename `RoundedCornerCalculator.calculated_x_hat`, and `calculated_y_hat`, to just `x_hat`, and `y_hat`
- [**breaking**] Rename `VectorFieldOperations.projection_length_on` to `projection_length_along`

### 🐛 Bug Fixes

- [**breaking**] Remove unused `arc_direction` parameter to RonudedCornerCalculator, add docstrings

### 💼 Other

- Fix `mypy` invocation
- Add generation of license notices from dependency packages
- Add a GitHub workflow for publishing documentation to GitHub Pages
- Generate a GitHub-like code coverage badge

### 📚 Documentation

- Fix README.md example, and add to doctests
- Add Sphinx documentation generation

### 🧪 Testing

- Specify float precision in doc tests (fixes failures in some environments)

## [0.1.0] - 2026-05-06
