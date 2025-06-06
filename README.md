[![Build Status](https://github.com/davewalker5/NatureRecorderPy/workflows/Python%20CI%20Build/badge.svg)](https://github.com/davewalker5/NatureRecorderPy/actions)
[![Coverage](https://codecov.io/gh/davewalker5/NatureRecorderPy/branch/main/graph/badge.svg?token=U86UFDVD5S)](https://codecov.io/gh/davewalker5/NatureRecorderPy)
[![GitHub issues](https://img.shields.io/github/issues/davewalker5/NatureRecorderPy)](https://github.com/davewalker5/NatureRecorderPy/issues)
[![Releases](https://img.shields.io/github/v/release/davewalker5/NatureRecorderPy.svg?include_prereleases)](https://github.com/davewalker5/NatureRecorderPy/releases)
[![License: MIT](https://img.shields.io/badge/License-mit-blue.svg)](https://github.com/davewalker5/NatureRecorderPy/blob/main/LICENSE)
[![Language](https://img.shields.io/badge/language-python-blue.svg)](https://www.python.org)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/davewalker5/NatureRecorderPy)](https://github.com/davewalker5/NatureRecorderPy/)

# Nature Recorder

Nature Recorder is an application for recording wildlife sightings, maintaining details of:

- Locations, with the following details:
  - Unique name
  - Address details
  - Latitude and longitude
- Categories, with the following details:
  - Category name e.g. birds, mammals
- Species, with the following details:
  - The category to which the species belongs
  - Species name
- Species sightings, consisting of:
  - The species, and by implication the category the species belongs to
  - Location
  - Date
  - Gender of the animals seen
  - Number of animals seen (optional)
  - Whether or not they were seen with young
- Conservation status information, consisting of:
  - Conservation schemes, acting as containers for a set of rating values
  - Conservation status ratings, values for the conservation status within a scheme
  - Species conservation status ratings, status ratings for a species with effective start and end dates
- Reports
  - Flexible reporting using Jupyter Notebooks

# Getting Started

Please see the [Wiki](https://github.com/davewalker5/NatureRecorderPy/wiki) for configuration details and instructions on how to run the application.

# Authors

- **Dave Walker** - _Initial work_

# Feedback

To file issues or suggestions, please use the [Issues](https://github.com/davewalker5/NatureRecorderPy/issues) page for this project on GitHub.

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
