from __future__ import annotations
from typing import *
from typing import Iterator
import itertools
import functools

T = TypeVar('T')
R = TypeVar('R')
IterT = TypeVar('IterT', bound=Iterator)

class Iter(Iterable[T]):
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
    
    def concat(self, other: Iterable[T]) -> Iter[T]:
        return Iter(itertools.chain(self, other))
    
    def count(self) -> int:
        return sum(1 for _ in self)
    
    def to_list(self) -> SList[T]:
        return SList(self._iter)
    def to_dict(self) -> Dict[T]:
        return dict(self._iter)
    def to_collection(self) -> IterCollection:
        return IterCollection(self.to_list())
    def collect(self, call: Callable[[Iterable], R]) -> R:
        return call(self)

class SList(list[T], Iter[T]):
    def iter(self) -> Iter[T]:
        return Iter(self)
    def append(self, item: T) -> SList[T]:
        super().append(item)
        return self
class SDict(dict[T], Iter[T]):
    def iter(self) -> Iter[T]:
        return Iter(self)

class IterCollection(Iter[T]):

    _collection = None

    def __init__(self, data: Collection[T]) -> None:
        if not isinstance(data, Collection):
            raise TypeError("iterator must be Collection!")
        self._collection = data
        super().__init__(self._collection)
    
    def __len__(self) -> int:
        return self._collection.__len__()
    
    def __getitem__(self, index: int) -> T:
        return self._collection.__getitem__(index)
    
    def __setitem__(self, index: int, value: T) -> None:
        return self._collection.__setitem__(index, value)
    
    def __reversed__(self) -> Iter[T]:
        return Iter(reversed(self._collection))