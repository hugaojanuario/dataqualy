import argparse
from collections.abc import Sequence

from dataqualy.config import load_config
from dataqualy.validator import run_validation


def build_parser() -> argparse.ArgumentParser:
    """Cria os comandos públicos do DataQualy."""
    parser = argparse.ArgumentParser(
        prog="dataqualy",
        description="Validador de qualidade para migrações de dados.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate = subcommands.add_parser(
        "validate",
        help="Executa as validações definidas em um arquivo YAML.",
    )
    validate.add_argument(
        "--config",
        required=True,
        help="Caminho do arquivo YAML de configuração.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Executa a interface de linha de comando."""
    args = build_parser().parse_args(argv)

    if args.command == "validate":
        config = load_config(args.config)
        run_validation(config)
        return 0

    return 2


# @hugaojanuario
