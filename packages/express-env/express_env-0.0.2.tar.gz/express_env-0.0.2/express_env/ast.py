from collections.abc import Sequence
from dataclasses import dataclass


def escape_bash(value: str) -> str:
    if " " in value or '"' in value:
        escaped = value.replace("$", "\\$").replace('"', '\\"')
        return f'"{escaped}"'
    return value


@dataclass(frozen=True)
class Command:
    command: str
    args: Sequence[str] = ()

    def render(self):
        return " ".join([self.command, *map(escape_bash, self.args)])


@dataclass(frozen=True)
class CommandSubstitution:
    command: Command


@dataclass(frozen=True)
class ConstValue:
    value: str


@dataclass(frozen=True)
class EnvironmentAssigment:
    variable: str
    value: CommandSubstitution | ConstValue
