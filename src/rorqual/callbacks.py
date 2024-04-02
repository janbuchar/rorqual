from typing import Any, Callable, Generic, ParamSpec

TArgs = ParamSpec("TArgs")


class CallbackList(Generic[TArgs]):
    def __init__(self) -> None:
        self.callbacks = list[Callable[TArgs, Any]]()

    def register(self, callback: Callable[TArgs, Any]) -> None:
        self.callbacks.append(callback)

    def __call__(self, *args: TArgs.args, **kwargs: TArgs.kwargs) -> Any:
        for callback in self.callbacks:
            callback(*args, **kwargs)
