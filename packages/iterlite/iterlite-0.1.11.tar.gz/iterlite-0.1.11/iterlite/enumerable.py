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
    _iter: Iterable[T] = None

    def __init__(self, iterator: Iterable[T]) -> None:
        self._iter = iterator
    
    def __iter__(self):
        return self._iter.__iter__()
    
    def __next__(self) -> T:
        return self._iter.__next__()

    def filter(self, predicate: Callable[[T], bool]) -> Iter[T]:
        return IterFilter(self, predicate)
    
    def map(self, func: Callable[[T], R]) -> Iter[R]:
        return IterMap(self, func)
    
    def first(self) -> Optional[T]:
        try:
            return next(self)
        except StopIteration:
            return None

    def flatten(self) -> Iter[T]:
        return Iter(itertools.chain.from_iterable(self))
    
    def reduce(self, f: Callable[[R, T], R], initial: Optional[R] = None) -> R:
        return functools.reduce(f, self, self.first() if initial is None else initial)
    
    def for_each(self, f: Callable[[T], None]) -> None:
        for item in self:
            f(item)
    
    def skip(self, n: int) -> Iter[T]:
        return IterSlice(self, n, None)
    
    def take(self, n: int) -> Iter[T]:
        return IterSlice(self, None, n)
    
    def slice(self, start: int, end: int) -> Iter[T]:
        return IterSlice(self, start, end)
    
    def nth(self, n: int) -> Optional[T]:
        return self.skip(n).first()
    
    def enumerate(self, start: int = 0) -> Iter[tuple[int, T]]:
        return Iter(enumerate(self, start))

    def group_by(self, key: Callable[[T], R]) -> Iter[tuple[R, Iter[T]]]:
        return IterGroupby(self, key)

    def batch(self, n: int):
        return self.enumerate() \
            .group_by(lambda x: x[0] // n) \
            .map(lambda x: x[1].map(lambda y: y[1]))
    
    def concat(self, other: Iterable[T]) -> Iter[T]:
        return Iter(itertools.chain(self, other))
    
    def count(self) -> int:
        return sum(1 for _ in self)
    
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

class IterMap(Iter[T], Generic[T, R]):

    def __init__(self, iterator: Iterable[T], f: Callable[[T], R]) -> None:
        super().__init__(iterator)
        self.func = f
    
    def __iter__(self):
        return map(self.func, self._iter)
    
    def __next__(self) -> T:
        return self.__next__()
    
class IterFilter(Iter[T], Generic[T]):
    def __init__(self, iterator: Iterable[T], predicate: Callable[[T], bool]) -> None:
        super().__init__(iterator)
        self.func = predicate
    
    def __iter__(self):
        return filter(self.func, self._iter)
    
    def __next__(self) -> T:
        return self.__next__()

class IterSlice(Iter[T], Generic[T]):
    def __init__(self, iterator: Iterable[T], start: int, end: int) -> None:
        super().__init__(iterator)
        self.start = start
        self.end = end
    
    def __iter__(self):
        if(self.end is None):
            return itertools.islice(self, self.start)
        if(self.start is None):
            return itertools.islice(self, self.end, None)
        return itertools.islice(self._iter, self.start, self.end)
    
    def __next__(self) -> T:
        return self.__next__()
    
class IterGroupby(Iter[T], Generic[T, R]):
    def __init__(self, iterator: Iterable[T], key: Callable[[T], R]) -> None:
        super().__init__(iterator)
        self.key = key
    
    def __iter__(self):
        return map(lambda pair: (pair[0], Iter[T](pair[1])), itertools.groupby(self._iter, self.key))
    
    def __next__(self) -> T:
        return self.__next__()

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