from __future__ import annotations
from typing import *
from typing import Iterator
import itertools
import functools

T = TypeVar('T')
R = TypeVar('R')
K = TypeVar('K')
V = TypeVar('V')
IterT = TypeVar('IterT', bound=Iterator)

class Iter(Iterable[T], Generic[T]):
    """
    Iterable class, which can be used as an iterator.
    """
    _data: Iterable[T] = []
    _iter: Iterator[T] = None

    def __init__(self, iterator: Iterable[T]) -> None:
        self._data = iterator
        self._iter = iter(self._data)
    
    def __iter__(self) -> Iter[T]:
        return Iter(self._data)
    
    def __next__(self) -> T:
        return self._iter.__next__()

    def filter(self, predicate: Callable[[T], bool]) -> Iter[T]:
        return Iter(filter(predicate, self))
    
    def map(self, func: Callable[[T], R]) -> Iter[R]:
        return Iter(map(func, self))
    
    def first(self) -> Optional[T]:
        try:
            return next(self)
        except StopIteration:
            return None

    def flatten(self) -> Iter[T]:
        return Iter(itertools.chain.from_iterable(self))
    
    def reduce(self, f: Callable[[R, T], R], initial: Optional[R] = None) -> R:
        return functools.reduce(f, self, next(self) if initial is None else initial)
    
    def for_each(self, f: Callable[[T], None]) -> None:
        for item in self:
            f(item)
    
    def skip(self, n: int) -> Iter[T]:
        return Iter(itertools.islice(self, n, None))
    
    def take(self, n: int) -> Iter[T]:
        return Iter(itertools.islice(self, n))
    
    def nth(self, n: int) -> Optional[T]:
        return self.skip(n).first()
    
    def slice(self, start: int, end: int) -> Iter[T]:
        return self.skip(start).take(end - start)
    
    def concat(self, other: Iterable[T]) -> Iter[T]:
        return Iter(itertools.chain(self, other))
    
    def count(self) -> int:
        return sum(1 for _ in self)
    
    def group_by(self, key: Callable[[T], R]) ->Iter[tuple[R, Iter[T]]]:
        return Iter(itertools.groupby(self, key))
    
    def pairwise(self) -> Iter[tuple[T, T]]:
        return Iter(itertools.pairwise(self))

    def to_list(self) -> SList[T]:
        return SList(self)
    def to_dict(self, f: Callable[[T], tuple[K, V]]) -> SDict[K, V]:
        return SDict[K, V](self.map(f))
    def to_collection(self):
        return IterCollection(self.to_list())
    def collect(self, call: Callable[[Iterable], R]) -> R:
        return call(self)

class SList(list[T], Iter[T], Generic[T]):
    """
    Smart list, which can be used as an iterator.
    """
    def iter(self) -> Iter[T]:
        return Iter(self)
    def append(self, item: T) -> SList[T]:
        super().append(item)
        return self
    
class SDict(dict[K, V], Iter[K], Generic[K, V]):
    """
    Smart dict, which can be used as an iterator.
    """
    def iter(self) -> Iter[T]:
        return Iter(super().keys())
    def keys(self) -> Iter[K]:
        return Iter(super().keys())
    def values(self) -> Iter[V]:
        return Iter(super().values())
    def items(self) -> Iter[tuple[K, V]]:
        return Iter(super().items())
    

class IterCollection(Iter[T], Generic[T]):
    _collection = None

    def __init__(self, data: Collection[T]) -> None:
        if not isinstance(data, Collection):
            raise TypeError("iterator must be Collection!")
        self._collection = data
        super().__init__(self._collection)
    
    def __len__(self) -> int:
        return self._collection.__len__()
    
    def len(self) -> int:
        return self.__len__()
    
    def __getitem__(self, index: int) -> T:
        return self._collection.__getitem__(index)
    
    def __setitem__(self, index: int, value: T) -> None:
        return self._collection.__setitem__(index, value)
    
    def __reversed__(self) -> Iter[T]:
        return Iter(reversed(self._collection))
    
    def reversed(self) -> Iter[T]:
        return self.__reversed__()