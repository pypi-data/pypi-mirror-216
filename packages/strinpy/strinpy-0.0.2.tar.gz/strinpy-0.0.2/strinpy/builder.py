import typing as _t
import itertools
import asyncio
Value = _t.Union[str, int, float, bool, None, _t.List, _t.Tuple, _t.List['Value']]

EMPTY_TUPLE = tuple()

V = _t.TypeVar('V', bound=Value)

class Formatter:
    def format_value(self, value: _t.Any) -> _t.Tuple[str]:
        if value in (False, None):
            return EMPTY_TUPLE
        if isinstance(value, list):
            return tuple(itertools.chain.from_iterable(map(self.format_value, value)))
        elif callable(value):
            return value()
        return (str(value),)

class Builder(_t.Generic[V]):
    def __init__(self, formatter: Formatter = Formatter()) -> None:
        self.formatter = formatter

    def format_value(self, value: V | Value) -> _t.Tuple[str]:
        if value == False:
            return EMPTY_TUPLE
        if isinstance(value, list):
            return tuple(itertools.chain.from_iterable(map(self.format_value, value)))
        elif callable(value):
            return value()
        return (str(value),)

    def build(self, value: V) -> str:
        parts = self.format_value(value)
        return ''.join(parts)


class AsyncBuilder(Builder[V]):

    async def format_value(self, value: V | Value) -> _t.Tuple[str]:
        if value == False:
            return EMPTY_TUPLE
        if isinstance(value, list):
            return tuple(itertools.chain.from_iterable(await asyncio.gather(*map(self.format_value, value))))
        elif callable(value):
            return value()
        return (str(value),)

    async def build(self, value: V) -> str:
        parts = await self.format_value(value)
        return ''.join(parts)


builder = Builder()
build: _t.Callable[[Value], str] = builder.build

abuilder = Builder()
abuild: _t.Callable[[Value], str] = abuilder.build
