"""Throttle function executions
"""
import functools
import queue
import threading
from enum import Enum
from typing import Any, Callable


class cap_exec_rate:
    """cap the execution rate of a function

    This class prevents a function from being executed too often. This
    class executes a function in another thread. Once it executes a
    function, it starts a timer. If the function is called again
    through this class while the timer is still running, this class
    does not execute the function immediately. Instead, this class
    executes the function after the timer goes off.

    The function might be called multiple times through this class
    while the timer is running. After the timer goes off, this class
    only executes the function once.

    Parameters
    ----------
    func : callable
        A function or any callable object to be executed not too often
    pause_time : float
        The length of time [second] to be waited after an execution of
        the `func` before the next execution. If the `func` is called
        through this class once or more times within this time length
        after an execution, it will be executed once after this time
        length passes.
    daemon : bool
        whether the thread which executes the function and sets the
        timer is daemonic. If `False`, the Python program doesn't exit
        until the thread ends; the method `end()` needs to be called;
        the function will be executed one last time if it has been
        called but not executed. If `True`, the thread can be abruptly
        stopped at the end of Python program; the function that has
        been called but not executed will not be executed.

    """

    def __init__(
        self, func: Callable[[], Any], pause_time: float = 1.0, daemon: bool = False
    ):
        self.func = func
        self.pause_time = pause_time
        self.daemon = daemon

        self.queue = queue.Queue[Message]()
        config = Config(func, self.queue, pause_time)
        self.machine = threading.Thread(
            target=state_machine, args=(config,), daemon=daemon
        )
        self.machine.start()

    def __call__(self) -> None:
        """call the function

        The number of executions of the function is capped
        """
        self.queue.put(Message.FUNC_CALLED)

    def end(self) -> None:
        """end using this class

        The function will be executed immediately if it is waiting for
        the timer. This method returns after the function is executed
        and the thread joins.

        """
        self.queue.put(Message.EXIT)
        self.machine.join()


class Message(Enum):
    FUNC_CALLED = 1
    TIMER_GOES_OFF = 2
    EXIT = 3


class Config:
    """Configuration of the state"""

    def __init__(
        self, func: Callable[[], Any], queue: queue.Queue[Message], pause_time: float
    ):
        self.func = func
        self.queue = queue
        self.pause_time = pause_time


def state_machine(config: Config) -> None:
    """the entry function to be executed in a thread"""
    state: State = Active(config)
    while not state.end:
        state = state()


class State:
    """The base class of the states"""

    end: bool = False

    def __init__(self, config: Config):
        self.config = config

    def __call__(self) -> 'State':
        message = self.config.queue.get()
        if message == Message.FUNC_CALLED:
            return self.func_called()
        elif message == Message.TIMER_GOES_OFF:
            return self.timer_goes_off()
        elif message == Message.EXIT:
            return self.exit_()
        else:
            raise ValueError('unknown message: {!r}'.format(message))

    def func_called(self) -> 'State':
        raise NotImplementedError

    def timer_goes_off(self) -> 'State':
        raise NotImplementedError

    def exit_(self) -> 'State':
        raise NotImplementedError


class Active(State):
    """Active state

    The timer is not running. The function can be executed immediately
    if it is called.
    """

    end = False

    def __init__(self, config: Config):
        super().__init__(config)

    def func_called(self) -> State:
        self.config.func()
        return Pause(self.config)

    def exit_(self) -> State:
        return Exit(self.config)


def timer_end(queue: queue.Queue[Message]) -> None:
    queue.put(Message.TIMER_GOES_OFF)


class Pause(State):
    """Pause state. The function has not been called

    The timer is running. The function has not been called. It won't
    be executed immediately when it is called.
    """

    end = False

    def __init__(self, config: Config):
        super().__init__(config)
        self.timer = threading.Timer(
            self.config.pause_time, functools.partial(timer_end, self.config.queue)
        )
        self.timer.start()

    def func_called(self) -> State:
        return PauseCalled(self.config, self.timer)

    def timer_goes_off(self) -> State:
        return Active(self.config)

    def exit_(self) -> State:
        self.timer.cancel()
        return Exit(self.config)


class PauseCalled(State):
    """Pause state. The function has been called

    The timer is running. The function has been called. The function
    won't be executed until the timer goes off.
    """

    end = False

    def __init__(self, config: Config, timer: threading.Timer):
        super().__init__(config)
        self.timer = timer

    def func_called(self) -> State:
        return self

    def timer_goes_off(self) -> State:
        self.config.func()
        return Pause(self.config)

    def exit_(self) -> State:
        self.timer.cancel()
        self.config.func()
        return Exit(self.config)


class Exit(State):
    """Exit state"""

    end = True

    def __init__(self, config: Config):
        super().__init__(config)
