''' Hashing related modules '''
from __future__ import annotations
from typing import TypeGuard
from collections.abc import Hashable

__all__ = ("is_hashable",)

def is_hashable(obj:object) -> TypeGuard[Hashable]:
    ''' Returns whether it is a Hashable object.  Evaluates if it is an instance
    of the Hashable class (from collections.abc) otherwise tries to hash it. '''
    # If it is Hashable, go ahead return it
    if isinstance(obj, Hashable):
        return True
    # Try to hash it, if it successful return True otherwise return False.
    try:
        hash(obj)
        return True
    except TypeError:
        return False
