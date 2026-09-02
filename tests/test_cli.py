from unittest.mock import Mock, patch

from dataqualy.cli import main


def test_validate_command_loads_config_and_runs_validation():
    config = {"migration": {"name": "example"}}

    with (
        patch("dataqualy.cli.load_config", return_value=config) as load_config,
        patch("dataqualy.cli.run_validation", Mock()) as run_validation,
    ):
        exit_code = main(["validate", "--config", "configs/example.yml"])

    assert exit_code == 0
    load_config.assert_called_once_with("configs/example.yml")
    run_validation.assert_called_once_with(config)


# @hugaojanuario
