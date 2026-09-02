import argparse
from collections.abc import Sequence

from dataqualy.config import load_config
from dataqualy.report import write_html_report
from dataqualy.validator import run_validation


def build_parser() -> argparse.ArgumentParser:
    """Cria os comandos públicos do DataQualy."""
    parser = argparse.ArgumentParser(prog="dataqualy", description="Validador de migrações.")
    subcommands = parser.add_subparsers(dest="command", required=True)
    validate = subcommands.add_parser("validate", help="Valida usando um YAML.")
    validate.add_argument("--config", required=True, help="Arquivo YAML.")
    validate.add_argument(
        "--report", default="reports/validation-report.html",
        help="Caminho do relatório HTML.",
    )
    subcommands.add_parser("gui", help="Abre a interface gráfica.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Executa a interface de linha de comando."""
    args = build_parser().parse_args(argv)
    if args.command == "gui":
        from dataqualy.gui import launch_gui

        launch_gui()
        return 0
    if args.command == "validate":
        report = run_validation(load_config(args.config))
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
