import logging
from collections.abc import MutableMapping
from typing import (
    Optional, Union, Self, Generator
)
from itertools import zip_longest

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# FlatJson class

class FlatJson(MutableMapping):
    """
    `FlatJson` object is a flat representation of nested JSON-like data with 
    Pandas `Series` index-like label and filesystem path-like label access and 
    manipulation for nested JSON-like data. Primarily used to efficently 
    transform Pandas `Series` with MultiIndex index to nested JSON-like (dict, 
    list) object and nested JSON-like data to flat Pandas `Series` with 
    MultiIndex index.

    Labels need to be tuples or path-like strings. The default separator for 
    path-like text labels is ``/``, but can be configured by constructor or 
    updated by calling :meth:`FlatJson.set_keypath_separator`.

    Note that `FlatJson` provides :meth:`FlatJson.to_series()` to prepare 
    JSON-like data for efficiently creating Pandas `Series` object with data 
    MultiIndex index allowing to efficiently transform nested JSON-like object 
    to Pandas `Series`.

    Note that `FlatJson` provides :meth:`FlatJson.to_json()` to efficiently 
    create nested JSON-like object from flat tuple-like label dictionary. 
    Alternatively, `FlatJson` can be used as the target dictionary-like class when 
    calling `Series.to_dict(FlatJson)`, then `FlatJson.to_json()` can be called 
    to return nested json-like data for use with JSON:API applications.

    Parameters
    ----------
    data : json-like nested iterable, dict, or list
        Contains json-like data objects stored in `FlatJson`.
    keypath_separator : str, default ``/``
        Path-like separator for 
    keyfill_value : object, default ``''`` (empty string)

    Examples
    --------
    Constructing `FlatJson` from a nested dictionary.
    >>> import flatjsondict as fj
    >>> d = {'a': 1, 'b': {'c': 3}}
    >>> d_fj = fj.FlatJson(data=d)
    >>> d_fj
    {('a',): 1, ('b', 'c'): 3}

    Note that the nested objects are dictionaries hence all label keys are 
    string values.

    >>> d = {'a': 1, 'b': ['c', 3]}
    >>> d_fj = fj.FlatJson(data=d)
    >>> d_fj
    {('a',): 1, ('b', 0): 'c', ('b', 1): 3}

    Note that the labels keys for nested lists are integer values.

    >>> d = {'a': 1, 'b': ['c', 3]}
    >>> d_fj = fj.FlatJson(data=d)
    >>> d_fj.to_series()
    {('a', ''): 1, ('b', 0): 'c', ('b', 1): 3}

    Note that for nested object with varying nesting depth the label tuple 
    length is normalized (padded) when calling :meth:`FlatJson.to_series()`. 
    Such label length normalization prepares `FlatJson` data for efficient 
    creation of Pandas `Series` objects with MultiIndex index allowing to 
    transform deeply nested JSON object data to Pandas `Series`.

    Constructing nested json-like data from `FlatJson`-like dictioaries.
    >>> import flatjsondict as fj
    >>> d = {('a', ''): 1, ('b', 0): 'c', ('b', 1): 3}
    >>> d_fj = fj.FlatJson(data=d)
    >>> d_fj.to_json()
    {'a': 1, 'b': ['c', 3]}
    >>> d_fj.paths()
    ['a', 'b/0', 'b/1']

    Constructing `FlatJson` from Pandas `Series.to_dict()`.
    >>> import pandas as pd
    >>> import flatjsondict as fj
    >>> d = {('a', ''): 1, ('b', 0): 'c', ('b', 1): 3}
    >>> ds = pd.Series(d)
    >>> ds.to_dict(fj.FlatJson)
    {('a',): 1, ('b', 0): 'c', ('b', 1): 3}

    >>> ds.to_dict(fj.FlatJson).to_json()
    {'a': 1, 'b': ['c', 3]}

    Note that you can pass `FlatJson` to Pandas `Series.to_dict(FlatJson)` 
    to directly derive `FlatJson` from Pandas `Series` data. Then use
    `FlatJson.to_json()` to return nested JSON-like data.
    """

    _COERCE = list, set, tuple, dict
    _ARRAYS = list, set, tuple

    # -------------------------------------------------------------------------
    # Constructors

    def __init__(
        self,
        data = None,
        keypath_separator: str = '/',
        keyfill_value: object = ''
    ) -> None:
        logger.debug('original data type: %s', type(data))
        self.original_type = type(data)
        if self.original_type in self._ARRAYS:
            data = {i: value for i, value in enumerate(data)}
        elif self.original_type in (dict,):
            data = self.__parse_dict(data, keyfill_value = keyfill_value)
        else:
            self.original_type = dict
            logger.debug(
                'Setting self.original_type data type to %s '\
                'for source data type %s', self.original_type, type(data)
            )
        super().__init__()
        self._keypath_separator = keypath_separator
        self._keyfill_value = keyfill_value
        self._values = dict()
        self.__update(data)

    def __contains__(self, key) -> bool:
        """Return boolean indicating if key is in `FlatJson`."""
        if self.__has_keypath_separator(key):
            return key in self.paths()
        elif isinstance(key, str):
            return key in self._values
        else:
            return key in self.keys()

    def __delitem__(self, key) -> None:
        """
        Delete the item for the specified key.

        Parameters
        ----------
        key : tuple, str
            Label tuple or path-like string.

        Raises
        ------
        KeyError
            If the key is not in `FlatJson`.
        """
        keys = self.__parse_keys(key)

        if len(keys) > 1:
            pk, ck = keys[0], keys[1:]
            if pk not in self._values:
                raise KeyError
            del self._values[pk][ck]
        else:
            if keys[0] not in self._values:
                raise KeyError
            del self._values[keys[0]]

    def __eq__(self, other: object) -> bool:
        """Return `FlatJson` equal to other."""
        if isinstance(other, (dict, list)):
            return self._as_json() == other
        elif not isinstance(other, self.__class__):
            raise TypeError
        return self._as_json() == other._as_json()

    def __ne__(self, other: object) -> bool:
        """Return `FlatJson` not Equal to other."""
        return not self.__eq__(other)

    def __iter__(self) -> iter:
        """Iterate over the `FlatJson`."""
        return iter(self.keys())

    def __len__(self) -> int:
        """Return the number of items in `FlatJson`."""
        return len(self.keys())

    def __reduce__(self) -> tuple:
        """Return state information for pickling `FlatJson`"""
        return type(self), (
            self.to_json(),
            self._keypath_separator,
            self._keyfill_value
        )

    def __str__(self) -> str:
        """Return the string value of the `FlatJson` instance."""
        return '{{{}}}'.format(', '.join(
            ['{!r}: {!r}'.format(k, self[k]) for k in self.keys()]))

    def __repr__(self) -> str:
        """Return the string representation of the `FlatJson` instance."""
        return '<{} id={} {}>"'.format(
            self.__class__.__name__,
            id(self),
            str(self)
        )

    def __getitem__(self, key: Union[tuple, str]) -> object:
        """Implement evaluation of self[key] for `FlatJson`."""
        values = self._values
        keys = self.__parse_keys(key)
        for subkey in keys:
            values = values[subkey]
        return values

    def __setitem__(self, key, value) -> None:
        """Dynamically build nested `FlatJson`."""
        if isinstance(value, self._COERCE) and \
                not isinstance(value, FlatJson):
            value = self.__class__(
                value,
                self._keypath_separator,
                self._keyfill_value
            )

        keys = self.__parse_keys(key)

        if keys[1:]:
            pk, ck = keys[0], keys[1:]
            if pk not in self._values:
                if isinstance(pk, int):
                    self.original_type = list
                self._values[pk] = self.__class__(
                    {ck: value},
                    self._keypath_separator,
                    self._keyfill_value
                )
                return
            elif not isinstance(self._values[pk], FlatJson):
                raise TypeError(
                    'Assignment to invalid type for key {}'.format(pk))
            self._values[pk][ck] = value
        else:
            if isinstance(keys[0], int):
                self.original_type = list
            self._values[keys[0]] = value

    def __update(self, data = None) -> None:
        """
        Derive `FlatJson` from a nested json-like data input.

        Parameters
        ----------
        data : dict, list or json-like
            Data used to populate the new `FlatJson`.

        """
        if isinstance(data, (Generator, zip)):
            logger.debug(
                'Converting %s type data source to dictionary and '\
                'deriving FlatJson with self.original_type set to %s',
                type(data),
                self.original_type
            )
            [
                self.__setitem__(k, v)
                 for k, v in 
                 self.__parse_dict(
                     dict(data),
                     keyfill_value = self._keyfill_value
                 ).items()
            ]
        else:
            [self.__setitem__(k, v) for k, v in data.items()]

    def __parse_keys(self, key) -> tuple:
        """
        Derive tuple with label keys from path-like label keys. Converts
        integer keys from path-like labels to integers.

        Returns
        -------
        tuple
            The tuple with label keys.
        """
        if isinstance(key, tuple):
            keys = key
        elif self.__has_keypath_separator(key):
            keys = tuple([
                int(subkey) if subkey.isdigit() 
                else subkey
                for subkey in key.split(self._keypath_separator)
            ])
        else:
            keys = tuple([key])
        return keys

    def __parse_dict(
        self,
        data: dict = None,
        keyfill_value: object = ''
    ) -> dict:
        """
        Derive dictionary without tuple-like label key padding values.

        Returns
        -------
        dict
            The dictionary without padded values in tuple-like label keys.
        """
        if all(isinstance(key, tuple) for key in data.keys()):
            return dict(zip(
                [key[:key.index(keyfill_value)] 
                 if keyfill_value in key 
                 else key for key in data.keys()],
                data.values()
            ))
        return data

    def __has_keypath_separator(self, key) -> bool:
        """Checks if the label is path-like key and contains the keypath separator."""
        return isinstance(key, str) and self._keypath_separator in key

    def _listkeys(self) -> list:
        """Return a list with `FlatJson` keys."""
        result = []
        for key, value in self._values.items():
            if isinstance(self._values[key], FlatJson):
                subkeys = self._values[key]._listkeys()
                for subkey in subkeys:
                    result.append(
                        [key] + subkey if isinstance(subkey, list)
                        else [subkey]
                    )
            else:
                result.append([key])
        return result

    def _as_dict(self) -> dict:
        """Return nested dictionary with data from `FlatJson`."""
        out = {}
        for key in self._values.keys():
            if isinstance(self._values[key], FlatJson) and key not in out:
                if self._values[key].original_type in self._ARRAYS:
                    out[key] = self._values[key].original_type(
                        self._values[key]._as_list()
                    )
                elif self._values[key].original_type == dict:
                    out[key] = self._values[key]._as_dict()
            else:
                if isinstance(self._values[key], FlatJson):
                    out[key] = self._values[key].original_type()
                else:
                    out[key] = self._values[key]
        return out

    def _as_list(self) -> list:
        """Return nested list with data from `FlatJson`."""
        out = []
        for key in self._values.keys():
            if isinstance(self._values[key], FlatJson):
                if self._values[key].original_type in self._ARRAYS:
                    out.append(self._values[key].original_type(self._values[key]._as_list()))
                elif self._values[key].original_type == dict:
                    out.append(self._values[key]._as_dict())
            else:
                if isinstance(self._values[key], FlatJson):
                    out.append(self._values[key].original_type())
                else:
                    out.append(self._values[key])
        return out

    def _as_json(self) -> Union[dict, list]:
        """Return nested dictionary or list with data from `FlatJson`."""
        if self.original_type in self._ARRAYS:
            return self._as_list()
        elif self.original_type in (dict,):
            return self._as_dict()

    def update(self, data = None, inplace: bool = True) -> Union[None, Self]:
        """
        Update or derive `FlatJson`.

        Parameters
        ----------
        data : dict, list or json-like
            Data used to update or derive new `FlatJson`.
        inplace : bool, default True
            If ``True``, performs operation inplace and returns None.

        Returns
        -------
        None or FlatJson
            None if ``inplace=True`` or `FlatJson` with updated data.
        """
        if inplace:
            self.__update(
                self.__class__(
                    data,
                    self._keypath_separator,
                    self._keyfill_value
                )._as_json()
             )
        else:
            json = self.copy()
            json.__update(
                self.__class__(
                    data,
                    self._keypath_separator,
                    self._keyfill_value
                )._as_json()
            )
            return json

    def set_keypath_separator(self, keypath_separator: str = '/') -> None:
        """Update keypath separator value."""
        for key in self.paths():
            if keypath_separator in key:
                raise ValueError(
                    'Key {!r} collides with keypath separator {!r}',
                    key,
                    keypath_separator
                )
        self._keypath_separator = keypath_separator
        for key in self._values.keys():
            if isinstance(self._values[key], FlatJson):
                self._values[key].set_keypath_separator(keypath_separator)

    def set_keyfill_value(self, keyfill_value: object = None) -> None:
        """Update label key keyfill value."""
        for key in self.keys():
            if keyfill_value in key:
                raise ValueError(
                    'Key {!r} collides with keyfill value {!r}',
                    key,
                    keyfill_value
                )
        self._keyfill_value = keyfill_value
        for key in self._values.keys():
            if isinstance(self._values[key], FlatJson):
                self._values[key].set_keyfill_value(keyfill_value)

    def clear(self) -> None:
        """Remove all items from the flat dictionary."""
        self._values.clear()

    def copy(self) -> Self:
        """Return a shallow copy of the flat dictionary."""
        return self.__class__(
            self._as_json(),
            self._keypath_separator,
            self._keyfill_value
        )

    def items(self) -> list:
        """Return a list with the `FlatJson` ``(key, value)`` pairs."""
        return [(k, self.__getitem__(k)) for k in self.keys()]

    def values(self) -> list:
        """Return a list of `FlatJson` values."""
        return [self.__getitem__(k) for k in self.keys()]

    def keys(self) -> list:
        """Return a list of `FlatJson` labels as tuple keys."""
        return list(map(tuple, self._listkeys()))

    def paths(self) -> list:
        """Return a list of `FlatJson` labels as path-like keys."""
        return [
            self._keypath_separator.join(map(str, item)) 
            if isinstance(item, list) 
            else item for item in self._listkeys()
        ]

    def to_series(self) -> dict:
        """
        Convert `FlatJson` to {(key, subkey, '') -> value} dict object.
        Return a dictionary of `FlatJson` data with padded label key tuples.
        """
        from itertools import zip_longest
        return dict(zip(
            zip_longest(
                *zip_longest(
                    *map(tuple, self._listkeys()),
                    fillvalue = self._keyfill_value
                )
            ),
            self.values()
        ))

    def to_json(self) -> Union[dict, list]:
        """Return nested json-like data from `FlatJson`."""
        if self.original_type in self._ARRAYS:
            return self._as_list()
        else:
            return self._as_dict()
