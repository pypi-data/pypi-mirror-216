from typing import Protocol, TextIO


class Namespace(Protocol):
    command: str
    config: TextIO
