Contribution Guidelines
-----------------------

This document describes requirements and guidelines for code style
in the webvirt_api project.

When contributing features, fixes or changes to this project, developers
should comply with the following requirements, testing and style guidelines.

#### Requirements

- Maximum **line length of 79**
- **Test coverage of 100%** (see [Testing](#testing))
- **Ordered imports**
    - Can be checked and fixed using [isort](https://pycqa.github.io/isort/)
- All source code **must pass [flake8](https://flake8.pycqa.org/en/latest/)
  and [black](https://github.com/psf/black) checks**
    - Can be checked and fixed using
      [autoflake](https://github.com/PyCQA/autoflake) and
      [black](https://github.com/psf/black)
- **Classes use proper names**
    - `class ProperName: pass`
- **Constants use uppercased snake_case names**
    - `A_CONSTANT = 1`
- **Everything else uses lowercased snake_case names**
    - `normal_variable = 10`

#### Testing Guidelines

- Any additions or changes to the codebase should be accompanied by new
  or modified unit tests which exercise all branches and lines in the
  project
- Unit tests should contain test code which exercises dynamic function of
  the application
- There should be **at least** one unit test for each API route in the
  project


#### Style Guidelines

- [Don't Repeat Yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
- Use descriptive, but concise, variable names
    - `i` could be `idx` or `index` to provide more clarity
- Use type hints, with the exception of `self`

#### Attribution

Since virtweb_api is licensed under the [Apache 2.0 license](LICENSE), a
[NOTICE](NOTICE) file is housed in this repository which denotes attributions
to the project.

Any contributors wishing to have attribution for the work they've done
should include their details in a change to the [NOTICE](NOTICE) file,
denoting where the work was done and by who. These changes will be
merged in as long as the author has provided contributions.
