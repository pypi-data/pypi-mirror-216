import pytest
from pydantic import BaseModel, Field, PrivateAttr
from typing import Any, ClassVar, FrozenSet, Optional, Set
from pydantic_dict import BaseModelDict


_unset_sentinel = object()


def singleton():
    return _unset_sentinel


Unset: None = Field(default_factory=singleton)


# from dataclasses import dataclass, field
from typing_extensions import Self

# K = TypeVar("K")
# V = TypeVar("V")


# @dataclass
# class CowDict(Generic[K, V]):
#     data: Dict[K, V] = field(default_factory=dict)

#     def __contains__(self, key) -> bool:
#         return key in self.data

#     def set(self, key, value) -> Self:
#         data = self.data.copy()
#         data[key] = value
#         return CowDict(data)

#     def update(self, more_data) -> Self:
#         data = self.data.copy()
#         data.update(more_data)
#         return CowDict(data)

#     def delete(self, key) -> Self:
#         if key not in self.data:
#             raise KeyError(f"'{key}' not in dictionary")

#         data = self.data.copy()
#         del data[key]
#         return CowDict(data)

#     def get(self, key, default):
#         return self.data.get(key, default)

#     def contains(self, key) -> bool:
#         return key in self


# motivation:
# if you work through implementing __getitem__ __getattribute__ get and finally
# __contains__, you will eventually arrive at the conclusion that, for
# performance concerns, it would be best if you could just query some
# containter type to see if a field is Unset or not. This is most evident when
# implementing __contains__.


class Meta(BaseModel):
    _default_unset: ClassVar[FrozenSet[str]]
    _unset: Set[str] = PrivateAttr(default_factory=set)

    def __init_subclass__(cls) -> None:
        cls._default_unset = frozenset(
            name
            for name, field in cls.__fields__.items()
            if field.default_factory == singleton
        )
        return super().__init_subclass__()

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        # filter fields that were set during __init__ by `Unset` by default.
        self._unset = set(
            field
            for field in self._default_unset
            if self.__dict__[field] == _unset_sentinel
        )

    def __contains__(self, key) -> bool:
        if key in self._unset:
            return False
        return key in self.__dict__

    def __len__(self) -> int:
        return len(self.__dict__) - len(self._unset)

    def __iter__(self):
        return set(self.__dict__).difference(self._unset).__iter__()

    def __setattr__(self, name, value):
        if name in self._unset and value != _unset_sentinel:
            self._unset.remove(name)
        return super().__setattr__(name, value)

    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)

    def __getitem__(self, name):
        item = self.__dict__[name]
        if item == _unset_sentinel:
            raise KeyError
        return item

    def get(self, key: str, default: Any = None) -> Any:
        if key not in self:
            return default
        return self[key]

    # def __getattribute__(self, __name: str) -> Any:
    #     # must retrieve attributes through super to avoid infinite recursion
    #     attr = super().__getattribute__(__name)
    #     default_unset = super().__getattribute__("_default_unset")
    #     # slow path
    #     if __name in default_unset and attr == _sentinel:
    #         raise AttributeError

    #     return attr


class Foo(Meta):
    set: Optional[int] = Unset
    unset: Optional[int] = Unset


#     class Config(BaseModel.Config):
#         extra = "allow"
#         allow_mutation = False


# class Bar(BaseModelDict):
#     set: Optional[int] = Unset
#     unset: Optional[int] = Unset


# def test_access_other_var(m: BaseModel):
#     x = m.set


# from timeit import timeit

# foo = Foo(set=42)
# bar = Bar(set=42)
# times = 100_000

# foo_time = timeit(lambda : test_access_other_var(foo), number=times)
# bar_time = timeit(lambda: test_access_other_var(bar), number=times)

# print(f"{foo_time}")
# print(f"{bar_time}")
# print(f"foo faster: {bar_time / foo_time:.5f}"  if foo_time < bar_time else f"bar faster: {foo_time / bar_time:.5f}")


def test_it_works():
    foo = Foo(set=42)
    assert "unset" not in foo
    print([k for k in foo])
    foo["unset"] = 52
    foo.unset = 42
    print(foo.__dict__)
    print(foo._unset)
