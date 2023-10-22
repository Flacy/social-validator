# Social validator

![CI](https://github.com/flacy/social-validator/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/Flacy/social-validator/graph/badge.svg?token=IX9AMG6L9F)](https://codecov.io/gh/Flacy/social-validator)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/social-validator)
![License](https://img.shields.io/github/license/flacy/social-validator)

### ❓ What's this
This is a library for validating data from social networks and messengers,
such as identifiers, usernames, etc.

### ⚡ Motivation
The motivation for creating this library was derived from the fact that there
is no single database to determine the restrictions of each service.
Accordingly, in order to validate the data correctly, you need to deep down
into the documentation, but sometimes even these data are not specified in it,
and you need to test the validation manually. This library is designed to
solve this problem. *Unfortunately, only for python ;(*

### 💽 Installation
You can use [pip](https://github.com/pypa/pip) or
[fext](https://github.com/fextpkg/cli) to install the library:
```shell
fext install social-validator
```

### ✨ Usage
The interface for validating the values of **each service** looks like this:
```python
from social_validator import telegram

# Functions starting with "is" are used
# only to check and get boolean value.
telegram.is_valid_id("test_user_id")  # True

# Functions starting with "validate" are used for full-fledged validation, they
# format and raise social_validator.exceptions.ValidationError if validation failed.
telegram.validate_id("test_user_ID")  # "test_user_id"

# Note: Each validation function is based on check functions, which means that
# for each validation there is an analog that only returns boolean value, but not vice versa.
telegram.validate_command("cmd") and telegram.is_valid_command("cmd")
```
Documentation for each method is available via docstrings.
If you really need documentation as a separate page, please open issue.

### ⚠️ Roadmap
The project is under development and is moving to a stable version.
To track the status, you can [follow the link](https://github.com/users/Flacy/projects/1).

### 🛠️ Contributing
If you want to help with development, or want to see some feature, or fix a
bug, please open issue with the appropriate label first.