"""Utilities for measuring memory usage."""
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
from collections import deque
from itertools import chain
from sys import getsizeof, stderr

try:
    from reprlib import repr  # pylint: disable=redefined-builtin
except ImportError:  # pragma: defer to python
    pass

from . import public


@public
def total_size(obj, handlers=None, verbose=False):  # noqa: C901
    """Returns the approximate memory footprint an object and all of its contents.

    See `recipe <https://code.activestate.com/recipes/577504/>`__ for original.

    :param obj: object to measure size of
    :type  obj: object
    :param handlers: handlers to iterate over contents of containers, defaults to None
    :type  handlers: dict, optional
    :param verbose: whether to print verbose output, defaults to False
    :type  verbose: bool, optional
    :return: approximate memory footprint in bytes
    :rtype:  int

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}
    """
    if handlers is None:
        handlers = {}

    def dict_handler(_dict):  # pragma: defer to python
        return chain.from_iterable(_dict.items())

    all_handlers = {
        tuple: iter,
        list: iter,
        deque: iter,
        dict: dict_handler,
        set: iter,
        frozenset: iter,
    }
    all_handlers.update(handlers)  # user handlers take precedence
    seen = set()  # track which object id's have already been seen
    default_size = getsizeof(0)  # estimate sizeof object without __sizeof__

    def sizeof(obj):
        if id(obj) in seen:  # pragma: defer to python
            return 0
        seen.add(id(obj))
        size_total = getsizeof(obj, default_size)

        if verbose:
            print(size_total, type(obj), repr(obj), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(obj, typ):
                size_total += sum(map(sizeof, handler(obj)))
                break
        return size_total

    return sizeof(obj)
