# loggy
A simple logging utility.

<img src="https://img.shields.io/github/issues/mattdood/loggy"
    target="https://github.com/mattdood/loggy/issues"
    alt="Badge for GitHub issues."/>
<img src="https://img.shields.io/github/forks/mattdood/loggy"
    target="https://github.com/mattdood/loggy/forks"
    alt="Badge for GitHub forks."/>
<img src="https://img.shields.io/github/stars/mattdood/loggy"
    alt="Badge for GitHub stars."/>
<img src="https://img.shields.io/github/license/mattdood/loggy"
    target="https://github.com/mattdood/loggy/raw/master/LICENSE"
    alt="Badge for GitHub license, MIT."/>
<img src="https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2Fmattdood%2Floggy"
    target="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fmattdood%2Floggy"
    alt="Badge for sharable Twitter link."/>
[![Pytest](https://github.com/mattdood/loggy/actions/workflows/ci.yml/badge.svg)](https://github.com/mattdood/loggy/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/get-loggy.svg)](https://badge.fury.io/py/get-loggy)

## Installation
To install the package locally use the following:

```
pip install get-loggy
```

## Features
* Color support
* Custom color support (advanced)
* Add additional logging levels
* Optional log stream vs. log file
* Log record format
* Package level logging

## Usage
Loggy exists as a simple interface for some standard logging in Python.
This is done at the package level, not by name.

### Basic instantiation
A basic logger may look like this, defaulting to the "info" level logging.

```python
from loggy import loggy

log = loggy.get_loggy()

log.info("Something")
```

```bash
>>> 2022-06-21 20:16:39 PM PDT | INFO | Something | (<stdin>:1:<module>) |
```

### Using color
Colors are supported as well, though not for use with log files. Color and
log files are mutually exclusive, as the color codes would clutter the logs.

```python
log = loggy.get_loggy(use_color=True)
```

### Writing to files
File handlers are initiated using a dictionary of configurations for the file,
this gives more granular control over file based logging. This is passed
directly to the `FileHandler()` instantiation.

The below example creates a log file with append mode.

```
file_config = {"filename": "some-log-file.log", "mode": "a"}
log = loggy.get_loggy(log_file=file_config)
```

## Advanced usage
Custom colors can be created or added along with custom logging levels.
See the [`conftest.py`](./conftest.py) for an example of custom formatter
and ['test_loggy.py'](./test/test_loggy.py) to see how the colors are added
for a custom logging level.

## Running tests
[Pytest](https://pytest.org) is used as the test runner. To install and run tests
use the `requirements-dev.txt` and execute with `pytest`.

**Note:** Use a virtual environment. The steps to create one are left to the user,
there are many packages that accomplish this.

```bash
pip install -r requirements-dev.txt
pytest
```

