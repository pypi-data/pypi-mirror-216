from abc import ABC, abstractmethod
from asyncio import Task
from typing import Awaitable, Callable, Coroutine


class Serializable(ABC):
    @abstractmethod
    def to_bytes(self) -> bytes:
        pass


SendCoro = Callable[[Serializable], Awaitable[None]]
RecvCoro = Callable[[int], Awaitable[bytes | None]]
Callback = Callable[[], None]
CoroCallback = Callable[[], Awaitable[None]]
TaskCreator = Callable[[Coroutine], Task]


class IAircon(ABC):

    @abstractmethod
    def add_callback(self, callback: Callback) -> Callback:
        """Add a callback for when the state of the aircon changes."""
        pass
    
    @abstractmethod
    async def wait_until_ready(self) -> None:
        """Wait until the state of the aircon is fully initialised."""
        pass

    @abstractmethod
    async def set_temp(self, target_celsius: float) -> None:
        """Set the aircon's target temperature."""
        pass

    @abstractmethod
    async def turn_on(self) -> None:
        """Turn the aircon on."""
        pass

    @abstractmethod
    async def turn_off(self) -> None:
        """Turn the aircon off."""
        pass