from express_env.plugins.base import PluginLibrary

from .const import ConstPlugin
from .one_password import OnePasswordPlugin
from .vault import VaultPlugin

library = PluginLibrary()
library.register("const", ConstPlugin())
library.register("vault", VaultPlugin())
library.register("1password", OnePasswordPlugin())


def init_plugins():
    from ..render import render

    library.register_singledispatch(render.register)
