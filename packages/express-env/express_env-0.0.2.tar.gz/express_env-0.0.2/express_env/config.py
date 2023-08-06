import typing as t
from dataclasses import dataclass

import yaml

from .plugins import library
from .terminal import bold

EnvConfig: t.TypeAlias = t.Any | str | bool | int | float


@dataclass(frozen=True)
class Config:
    env: t.Mapping[str, EnvConfig]


def parse_env_config(key: str, value: t.Any) -> EnvConfig:
    match value:
        case str() | int() | float() as value:
            return library.get("const").forge({"value": value})
        case {"type": str() as type_, **rest}:
            try:
                plugin = library.get(type_)
            except KeyError:
                raise ValueError(
                    f"Unknown plugin {bold(type_)} for env variable {bold(key)}. "
                    f"Available plugins: {', '.join(map(bold, library.plugins_names))}"
                ) from None
            return plugin.forge(rest)
        case dict():
            raise ValueError(f"Missing type for env variable {bold(key)}")
        case _:
            raise ValueError(
                f"Invalid config for env variable {bold(key)}: {bold(value)}"
            )


def load(file: t.TextIO) -> Config:
    raw_config = yaml.safe_load(file)

    if "env" not in raw_config:
        raise ValueError("Config must contain env section")

    return Config(env={k: parse_env_config(k, v) for k, v in raw_config["env"].items()})
