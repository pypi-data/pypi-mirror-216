''' Module describes a FrozenDict '''
from __future__ import annotations
from collections.abc import Mapping, Hashable, Iterable, Iterator
from typing import TypeVar, Union, Any, Optional
from capi.tools.hashing import is_hashable

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
HV = TypeVar("HV", bound=Hashable)

__all__ = ("FrozenDict", "HashableFrozenDict",)

class FrozenDict(Mapping[K, V]):
    ''' A mapping of Keys to Values similar to a dictionary, however cannot
    be modified. '''

    __slots__ = ("_dct",)

    _dct: dict[K, V]
    ''' Back-end dictionary '''

    def __init__(self, item: Optional[Union[Mapping[K, V],
                                            Iterable[tuple[K, V]]]] = None,
                 **kwargs: Any) -> None:

        if item is not None and len(kwargs) != 0:
            raise TypeError("Must pass either an Iterable item of "
                            + "key-value pairs or Mapping or must pass"
                            + "key-word arguments (kwargs), not both.")
        elif item is not None:
            self._dct = dict(item)
        elif len(kwargs) != 0:
            self._dct = dict(kwargs)
        else:
            self._dct = dict()

    def __getitem__(self, __key: K) -> V:
        try:
            return self._dct.__getitem__(__key)
        except KeyError as err:
            raise err

    def __iter__(self) -> Iterator[K]:
        return self._dct.__iter__()

    def __len__(self) -> int:
        return self._dct.__len__()
    

class HashableFrozenDict(FrozenDict[K, HV], Hashable):
    ''' Like a FrozenDict, except hashable.  Requires all values are hashable
    as well. '''

    def __init__(self, item: Optional[Union[Mapping[K, HV],
                                            Iterable[tuple[K, HV]]]] = None,
                       **kwargs: Any) -> None:
        
        super().__init__(item, **kwargs)

        if not all((is_hashable(v) for v in self.values())):
            raise TypeError("All values should be hashable for HashableFrozenDicts.")

    def __hash__(self) -> int:
        try:
            return hash(self._dct.items())
        except TypeError as err:
            raise TypeError("Items may not be hashable.") from err
