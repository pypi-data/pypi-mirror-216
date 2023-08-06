import argparse
import sys
from typing import cast

from express_env.plugins import init_plugins

from .commands import generate
from .config import load


def main(args=sys.argv[1:]) -> None:
    parser = argparse.ArgumentParser(
        description="Express Env CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config", type=argparse.FileType("r"), default=".ee/default.yaml"
    )
    subparser = parser.add_subparsers(
        dest="command", description="subcommands", required=True
    )
    generate.configure_parser(subparser)

    namespace = parser.parse_args(args=args)

    try:
        config = load(namespace.config)
    except ValueError as e:
        print("Error while loading config: ", e.args[0])  # noqa: T201
        exit(1)
    init_plugins()

    try:
        if namespace.command == "generate":
            generate_namespace: generate.GenerateNamespace = cast(
                generate.GenerateNamespace, namespace
            )
            generate.command(config, generate_namespace, args)
    except Exception:
        print(f"Error while executing command, used config: {config}")  # noqa: T201
        raise


if __name__ == "__main__":
    main()
