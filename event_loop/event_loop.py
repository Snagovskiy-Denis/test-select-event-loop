import socket

from contextlib import suppress
from typing import Generator, NoReturn
from selectors import DefaultSelector, EVENT_READ
from inspect import isgenerator


_tasks = []
_selector = DefaultSelector()


def _wait_for(sock: socket.socket, subscriber: Generator) -> None:
    _selector.register(sock, EVENT_READ, subscriber)


def _run(task: Generator) -> None:
    assert isgenerator(task)
    with suppress(StopIteration):
        if maybe_socket := next(task):
            _wait_for(maybe_socket, task)


def create_task(generator: Generator) -> None:
    """Schedule background execution of a generator"""
    assert isgenerator(generator)
    _tasks.append(generator)


def loop(main: Generator) -> NoReturn:
    """Start the event loop that handles select syscalls"""
    create_task(main)
    while True:
        while _tasks:
            _run(_tasks.pop(0))

        try:
            events = _selector.select()
        except KeyboardInterrupt:
            exit()

        for selector_key, _ in events:
            _selector.unregister(selector_key.fileobj)
            _run(selector_key.data)
