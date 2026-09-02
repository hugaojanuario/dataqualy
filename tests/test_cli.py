from datetime import datetime
from unittest.mock import patch

from dataqualy.cli import main
from dataqualy.models import ValidationReport


def test_validate_command_generates_report(tmp_path):
    config = {"migration": {"name": "example"}}
    report = ValidationReport(
        migration_name="example",
        started_at=datetime(2026, 1, 1),
        finished_at=datetime(2026, 1, 1),
    )
    output = tmp_path / "report.html"

    with (
        patch("dataqualy.cli.load_config", return_value=config) as load_config,
        patch("dataqualy.cli.run_validation", return_value=report) as run_validation,
    ):
        exit_code = main(
            ["validate", "--config", "configs/example.yml", "--report", str(output)]
        )

    assert exit_code == 0
    assert output.exists()
    load_config.assert_called_once_with("configs/example.yml")
    run_validation.assert_called_once_with(config)


# @hugaojanuario
