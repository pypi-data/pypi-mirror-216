from __future__ import annotations

from functools import partial, wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Generic,
    TypeVar,
    final,
)

from typing_extensions import ParamSpec, override

from async_wrapper.task_group.base import BaseSoonWrapper, SoonValue

try:
    from anyio.abc import TaskGroup  # type: ignore
except ImportError:
    from typing import Any as TaskGroup


ValueT = TypeVar("ValueT")
ValueT_co = TypeVar("ValueT_co", covariant=True)
OtherValueT_co = TypeVar("OtherValueT_co", covariant=True)
ParamT = ParamSpec("ParamT")
OtherParamT = ParamSpec("OtherParamT")

__all__ = ["SoonWrapper", "wrap_soon", "get_task_group"]


@final
class SoonWrapper(
    BaseSoonWrapper[TaskGroup, ParamT, ValueT_co],
    Generic[ParamT, ValueT_co],
):
    @override
    def __new__(
        cls,
        func: Callable[OtherParamT, Awaitable[OtherValueT_co]],
        task_group: TaskGroup,
    ) -> SoonWrapper[OtherParamT, OtherValueT_co]:
        try:
            import anyio  # type: ignore # noqa: F401
        except ImportError as exc:
            raise ImportError("install extas anyio first") from exc

        return super().__new__(cls, func, task_group)  # type: ignore

    @override
    def __init__(
        self,
        func: Callable[ParamT, Awaitable[ValueT_co]],
        task_group: TaskGroup,
    ) -> None:
        super().__init__(func, task_group)

        def outer(
            result: SoonValue[ValueT_co],
        ) -> Callable[ParamT, None]:
            @wraps(self.func)
            def inner(*args: ParamT.args, **kwargs: ParamT.kwargs) -> None:
                partial_func = partial(self.func, *args, **kwargs)
                set_value_func = partial(_set_value, partial_func, result)
                task_group.start_soon(set_value_func)

            return inner

        self._func = outer

    @override
    def __call__(
        self,
        *args: ParamT.args,
        **kwargs: ParamT.kwargs,
    ) -> SoonValue[ValueT_co]:
        result: SoonValue[ValueT_co] = SoonValue()
        self._func(result)(*args, **kwargs)
        return result


def get_task_group() -> TaskGroup:
    try:
        from anyio import create_task_group  # type: ignore
    except ImportError as exc:
        raise ImportError("install extas anyio first") from exc
    return create_task_group()


async def _set_value(
    func: Callable[[], Coroutine[Any, Any, ValueT]],
    value: SoonValue[ValueT],
) -> None:
    result = await func()
    value.value = result


wrap_soon = SoonWrapper
