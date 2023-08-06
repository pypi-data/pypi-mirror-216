from collections.abc import Callable, Iterator
from typing import Any, Generic, Protocol, TypeVar

from express_env.ast import EnvironmentAssigment

ConfigType = TypeVar("ConfigType")


class Plugin(Protocol, Generic[ConfigType]):
    Config: type[ConfigType]

    def forge(self, config: dict[object, object]) -> ConfigType:
        ...

    def render(self, config: ConfigType, key: str) -> Iterator[EnvironmentAssigment]:
        ...


class PluginLibrary:
    _plugins: dict[str, Plugin]

    def __init__(self):
        self._plugins = {}

    def register(self, name: str, plugin: Plugin[Any]) -> None:
        self._plugins[name] = plugin

    def get(self, name: str) -> Plugin:
        return self._plugins[name]

    def register_singledispatch(
        self, register: Callable[[type, Callable], None]
    ) -> None:
        for plugin in self._plugins.values():
            register(plugin.Config, plugin.render)

    @property
    def plugins_names(self) -> list[str]:
        return list(self._plugins.keys())
