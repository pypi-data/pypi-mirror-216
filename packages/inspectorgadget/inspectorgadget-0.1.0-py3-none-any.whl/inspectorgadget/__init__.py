#
# MIT License
#
# Copyright (c) 2023 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
Inspector Gadget - Extended Python Inspection.

This module extends the python built-in :any:`inspect` module

* :any:`get_signature` - Get Signature as a string
* :any:`getsize` - Sum Size of `obj` and Members
"""

import inspect as _inspect
import sys
from gc import get_referents
from types import FunctionType, ModuleType


def get_signature(func, vars_=None, exclude=None):
    """
    Return signature of `func` as string.

    >>> def func(a, b=2):
    ...     return a + b
    >>> get_signature(func)
    'func(a, b=2)'

    In case of given variables `vars_` the caller equivalent is returned.

    >>> get_signature(func, {'a': 4, 'b': 2})
    'func(4)'
    >>> get_signature(func, {'a': 4, 'b': 9})
    'func(4, b=9)'

    This is useful in combination with :any:`vars()`.

    >>> def func(a, b=2):
    ...     print(get_signature(func, vars()))
    >>> func(10, b=8)
    func(10, b=8)

    Positional arguments:

    >>> def func(a, *b):
    ...     print(get_signature(func, vars()))
    >>> func("a", "b0", "b1")
    func('a', 'b0', 'b1')

    Keyword arguments (Please note, that the kwargs are sorted by name):

    >>> def func(a, **kwargs):
    ...     print(get_signature(func, vars()))
    >>> func("a", foo=4, bar=8)
    func('a', bar=8, foo=4)

    Parameters can be hidden via `exclude` by name or index.

    >>> def func(a, b, c, d=None, e=None):
    ...     print(get_signature(func, vars(), exclude=(0, "d", "g")))
    >>> func('a', 'b1', 'c2', 'd3', 'e4')
    func('b1', 'c2', e='e4')
    """
    # pylint: disable=too-many-nested-blocks,too-many-branches
    sig = _inspect.signature(func)
    name = func.__name__
    if vars_ is None:
        return f"{name}{str(sig)}"
    args = []
    if exclude is None:
        exclude = tuple()
    for idx, param in enumerate(sig.parameters.values()):
        if param.name in exclude or idx in exclude:
            continue
        if param.default is _inspect.Parameter.empty:
            if param.kind is _inspect.Parameter.VAR_POSITIONAL:
                args += [f"'{v}'" for v in vars_[param.name]]
            elif param.kind is _inspect.Parameter.VAR_KEYWORD:
                for k, value in sorted(vars_[param.name].items()):
                    if k in exclude:  # pragma: no cover
                        continue
                    args.append(f"{str(k)}={value!r}")
            else:
                args.append(repr(vars_[param.name]))
        else:
            try:
                value = vars_[param.name]
            except KeyError:  # pragma: no cover
                continue
            if param.default != value:
                args.append(f"{param.name}={value!r}")
    jargs = ", ".join(args)
    return f"{name}({jargs})"


def getsize(obj, blacklist=(type, ModuleType, FunctionType)):
    """
    Sum Size of `obj` and Members.

    >>> import sys
    >>> sys.getsizeof('a')
    50
    >>> sys.getsizeof('b')
    50
    >>> sys.getsizeof(('a', 'b'))  # doctest: +SKIP
    56
    >>> getsize(('a', 'b'))  # doctest: +SKIP
    156
    >>> def myfunc(a):
    ...     return a
    >>> getsize(myfunc)
    Traceback (most recent call last):
      ...
    TypeError: getsize() does not take argument of type: <class 'function'>
    """
    if isinstance(obj, blacklist):
        raise TypeError(f"getsize() does not take argument of type: {type(obj)}")
    seen_ids = set()
    size = 0
    objs = [obj]
    while objs:
        need_referents = []
        for item in objs:
            if not isinstance(item, blacklist) and id(item) not in seen_ids:
                seen_ids.add(id(item))
                size += sys.getsizeof(item)
                need_referents.append(item)
        objs = get_referents(*need_referents)
    return size
