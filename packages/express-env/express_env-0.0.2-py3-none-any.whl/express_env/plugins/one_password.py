import typing as t
from dataclasses import dataclass

from express_env import ast
from express_env.plugins.base import Plugin
from express_env.terminal import bold


@dataclass(frozen=True)
class OnePasswordEnv:
    vault: str
    item: str
    field: str


class OnePasswordPlugin(Plugin[OnePasswordEnv]):
    Config = OnePasswordEnv

    def forge(self, data: dict[object, object]) -> OnePasswordEnv:
        match data:
            case {
                "vault": str() as vault,
                "item": str() as item,
                "field": str() as field,
            }:
                return self.Config(vault, item, field)
        raise ValueError(
            f"Invalid config for {bold('1password')} plugin, "
            f"expected path and field: {bold(str(data))}"
        )

    @staticmethod
    def render(config: OnePasswordEnv, key) -> t.Iterator[ast.EnvironmentAssigment]:
        yield ast.EnvironmentAssigment(
            key,
            ast.CommandSubstitution(
                ast.Command(
                    "op",
                    [
                        "item",
                        "get",
                        config.item,
                        "--vault",
                        config.vault,
                        "--field",
                        config.field,
                    ],
                )
            ),
        )
