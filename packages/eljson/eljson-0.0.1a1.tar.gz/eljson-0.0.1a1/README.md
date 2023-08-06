# eljson

[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)

[![Build Status](https://github.com/blablatdinov/eljson/workflows/test/badge.svg?branch=master&event=push)](https://github.com/blablatdinov/eljson/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/blablatdinov/eljson/branch/master/graph/badge.svg)](https://codecov.io/gh/ablablatdinoveljson)
[![Python Version](https://img.shields.io/pypi/pyversions/eljson.svg)](https://pypi.org/project/eljson/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

This is how python package should look like!


## Features

- Object oriented work with `JSON`


## Installation

```bash
pip install elson
```


## Example

```python
from elson.strict_json import StrictJson
from elson.json import JsonDoc

StrictJson.from_string(
    JsonDoc.from_string(
        '{"hello": {"world": "!"}}',
    ),
    """
    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "hello": {
                "type": "object",
                "properties": {
                    "world": {"type": "string"}
                },
                "required": ["world"]
            }
        },
        "required": ["hello"]
    }
    """,
).path('$.hello.world')
```

## License

[MIT](https://github.com/blablatdinov/eljson/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [a10c1e14ff468a4328dbe36a6b9a6a321d80da60](https://github.com/wemake-services/wemake-python-package/tree/a10c1e14ff468a4328dbe36a6b9a6a321d80da60). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/a10c1e14ff468a4328dbe36a6b9a6a321d80da60...master) since then.
