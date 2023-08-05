"""blastpipe: A utility library for modern Python."""
# Copyright 2023 Ross J. Duff MSc
# The copyright holder licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import platform
import sys
from datetime import date
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("blastpipe")
except PackageNotFoundError:
    # package is not installed
    pass

PYMAJOR, PYMINOR, PYPATCH = map(int, platform.python_version_tuple())
minor_deprecation = {
    9: date(2025, 10, 1),
    10: date(2026, 10, 1),
    11: date(2027, 10, 1),
    12: date(2028, 10, 1),
}
python3_eol = minor_deprecation.get(PYMINOR, date(2008, 12, 3))

if date.today() > python3_eol:  # pragma: no cover
    raise RuntimeError(
        f"Python {PYMAJOR}.{PYMINOR}.{PYPATCH} is not supported" f"as of {python3_eol}."
    )


def public(obj):
    """Declares an object as public."""
    mod = sys.modules[obj.__module__]
    # pylint: disable=unnecessary-dunder-call
    if hasattr(mod, "__all__"):
        mod.__all__.append(obj.__name__)
    else:
        mod.__setattr__("__all__", [obj.__name__])
    return obj
