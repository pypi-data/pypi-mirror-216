from abc import ABC
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, TypeVar, Union

from aiogram import Bot, Dispatcher, Router

from axabc.db import AbstractUOWFactory

TUOW = TypeVar('TUOW', bound=AbstractUOWFactory)

class BaseHandlersGroup(ABC):
    __router: Union[None, Router] = None

    def __init__(
        self,
        bot: Bot,
        dp: Dispatcher,
        uowf: Union[TUOW, None] = None,
    ) -> None:
        self.router = proxy_router.get_group_observed_router(self)

        self.bot = bot
        self.dp = dp
        self.uowf = uowf

    @classmethod
    @property
    def router_collector(cls) -> Router:
        if not cls.__router:
            cls.__router = Router(name=cls.__name__)
        return cls.__router


OBSERVERS_NAME = [
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "inline_query",
    "chosen_inline_result",
    "callback_query",
    "shipping_query",
    "pre_checkout_query",
    "poll",
    "poll_answer",
    "my_chat_member",
    "chat_member",
    "chat_join_request",
    "error",
]

@dataclass
class FrozenHandler:
    observer_name: str

    args: Union[List[Any], tuple[Any]]
    kwargs: Dict[str, Any]
    fn: Any


class ProxyRouter(Router):
    _observers_name = OBSERVERS_NAME

    def __init__(self, *, name: str | None = None) -> None:
        self._cls_registrations: Dict[str, Dict[str, FrozenHandler]] = {}
        super().__init__(name=name)

    def proxy_observer(self, __name: str) -> Callable[[Any], Any]:
        def inner_wrapper(*args: Any, **kwargs: Dict[Any, Any]):
            def wrapper(fn: Callable[[Any], Any]) -> Any:
                clsname, methodname, *extra = fn.__qualname__.split('.')
                if not extra:
                    if clsname not in self._cls_registrations:
                        self._cls_registrations[clsname] = {}

                    self._cls_registrations[clsname][methodname] = FrozenHandler(
                        observer_name=__name,
                        args=args,
                        kwargs=kwargs,
                        fn=fn,
                    )

                return fn

            return wrapper

        return inner_wrapper

    def get_group_observed_router(self, group: BaseHandlersGroup) -> Router:
        cls = group.__class__
        clsname = cls.__name__
        router = Router(name=clsname)

        if clsname not in self._cls_registrations:
            raise NotImplementedError(f"{clsname} hasn't registered observers")

        for methodname, fh in self._cls_registrations[clsname].items():
            getattr(router, fh.observer_name)(*fh.args, **fh.kwargs)(getattr(group, methodname))

        return router


    def __getattribute__(self, __name: str) -> Any:
        if not __name.startswith('_') and __name in self._observers_name:
            return self.proxy_observer(__name)
        return super().__getattribute__(__name)


proxy_router = ProxyRouter()
