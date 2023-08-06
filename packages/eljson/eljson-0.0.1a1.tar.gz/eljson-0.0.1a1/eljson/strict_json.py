"""The MIT License (MIT).

Copyright (c) 2023 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
from typing import final

import attrs
import ujson
from jsonschema import validate

from eljson.json import Json


@final
@attrs.define(frozen=True)
class StrictJson(Json):
    """Json document validated by json-schema."""

    _origin: Json
    _json_schema: dict

    @classmethod
    def from_string(cls, origin: Json, raw_json: str):
        """Ctor for strings."""
        return cls(origin, ujson.loads(raw_json))

    def path(self, query: str):
        """Fetch nodes from json by jsonpath."""
        validate(instance=self._origin.path('$')[0], schema=self._json_schema)
        return self._origin.path(query)
