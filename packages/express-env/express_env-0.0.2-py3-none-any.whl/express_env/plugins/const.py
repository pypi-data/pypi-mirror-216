import typing as t
from dataclasses import dataclass

from express_env import ast
from express_env.plugins.base import Plugin


@dataclass(frozen=True)
class ConstEnv:
    value: str | bool | int | float
    type: t.Literal["const"] = "const"


class ConstPlugin(Plugin[ConstEnv]):
    Config = ConstEnv

    def forge(self, data: dict[object, object]) -> ConstEnv:
        match data:
            case str() | int() | float() as v:
                return self.Config(v)
            case {"value": str() | int() | float() as v}:
                return self.Config(v)
        raise ValueError(f"Invalid config for const plugin, expected value: {data}")

    @staticmethod
    def render(config: ConstEnv, name: str) -> t.Iterator[ast.EnvironmentAssigment]:
        yield ast.EnvironmentAssigment(
            name, ast.ConstValue(ConstPlugin._render_value(config.value))
        )

    @staticmethod
    def _render_value(value: str | bool | int | float) -> str:
        match value:
            case bool() as v:
                return "true" if v else "false"
            case float() as v:
                return "%.2f"
            case int() as v:
                return f"{v}"
            case str() as v:
                return v

        raise ValueError(
            f"Invalid value for const plugin, expected str, bool, int or float: {value}"
        )
