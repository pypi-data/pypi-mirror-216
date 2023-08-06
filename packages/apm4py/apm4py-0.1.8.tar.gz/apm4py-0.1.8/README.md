# apm4py
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg
)](https://www.python.org/downloads/release/python-374/)
[![apm4py](https://img.shields.io/badge/apm4py-v0.2.1-blue)](https://pypi.org/project/apm4py/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/lanalabs/apm4py/graphs/commit-activity)

apm4py is Python API for [Appian Process Mining](https://appian.com/). It focuses on resource management, but provides methods that can be used to access the processed data as well.

This package is still in initial development state. Anything may change at any time. The public API should not be considered stable.

## Installation

You can install apm4py directly from PyPi with e.g. 

```bash
$ pip install apm4py
```

# How to get started

To connect with an api at e.g. 'https://cloud-backend.lanalabs.com', first create an API with

```python
from apm4py import create_api

api = create_api('https', 'cloud-backend.lanalabs.com', API_KEY)
```

# Using the Command Line

Command line currently only supports uploading event logs. Four files for the event log have to be in one folder and follow the convention:
* event log CSV has "event" in the file name
* case attribute CSV has "case" in the file name
* event log semantics json have "event" in the file name
* case attribute log semantics json have "case" in the file name

See ./tests/data/incident_management as an example.

With that you can do 
`poetry run apm --name "Incident Management" tests/data/incident_management`

# Building and installing
```bash
poetry install
poetry build
pip install /dist/apm4py-0.1.7-py3-none-any.whl
```


# How to contribute

See the details in [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[Apache License 2.0](http://www.apache.org/licenses/)

