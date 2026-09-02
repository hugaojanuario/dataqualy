import argparse
from collections.abc import Sequence

from dataqualy.config import load_config
from dataqualy.report import write_html_report
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
    validate.add_argument(
        "--report",
        default="reports/validation-report.html",
        help="Caminho do relatório HTML.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Executa a interface de linha de comando."""
    args = build_parser().parse_args(argv)

    if args.command == "validate":
        config = load_config(args.config)
        report = run_validation(config)
        output = write_html_report(report, args.report)
        print(f"Relatório: {output.resolve()}")
        print(
            "Resultado: aprovado"
            if report.passed
            else f"Resultado: {report.issue_count} divergência(s)"
        )
        return 0 if report.passed else 1

    return 2


# @hugaojanuario
