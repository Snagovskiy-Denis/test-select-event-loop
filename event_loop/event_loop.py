import time

from contextlib import suppress
from typing import Generator, NoReturn
from selectors import DefaultSelector, EVENT_READ
from inspect import isgenerator


_waiting = []
_ready = []
_current_gen: Generator = None  # pyright: ignore

_selector = DefaultSelector()


def _run(gen: Generator) -> None:
    assert isgenerator(gen)
    global _current_gen
    _current_gen = gen
    with suppress(StopIteration):
        next(gen)


def read_ready(fileobj):
    _selector.register(fileobj, EVENT_READ, _current_gen)
    yield


def sleep(seconds: float):
    target = time.time() + seconds
    _waiting.append((target, _current_gen))
    yield


def create_task(generator: Generator) -> None:
    """Schedule background execution of a generator"""
    assert isgenerator(generator)
    _ready.append(generator)


def loop(main: Generator) -> NoReturn:
    """Start the event loop that handles select syscalls"""
    create_task(main)

    while True:
        while _ready:
            _run(_ready.pop(0))

        for target, gen in _waiting.copy():
            if time.time() > target:
                _waiting.remove((target, gen))
                _run(gen)

        try:
            events = _selector.select(-1)
        except KeyboardInterrupt:
            exit()

        for selector_key, _ in events:
            _selector.unregister(selector_key.fileobj)
            _run(selector_key.data)
