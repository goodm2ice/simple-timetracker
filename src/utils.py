from typing import Dict, TypeVar
from collections.abc import Iterable


K, V = TypeVar('K'), TypeVar('V')
def filter_dict_keys(obj: Dict[K, V], keys: Iterable[K]) -> Dict[K, V]:
    return { k: v for k, v in obj.items() if k not in keys }
