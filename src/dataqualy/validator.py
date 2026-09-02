from datetime import datetime
from typing import Any

from pyspark.sql import DataFrame, Row

from dataqualy.checks import (
    find_duplicate_keys,
    find_missing_records,
    find_value_differences,
)
from dataqualy.datasource import collect_jars, read_dataset
from dataqualy.models import CheckResult, ValidationReport
from dataqualy.rules import execute_rule
from dataqualy.spark import create_spark_session


def _row_to_dict(row: Row) -> dict[str, Any]:
    return {key: value for key, value in row.asDict(recursive=True).items()}


def _evaluate(
    dataframe: DataFrame,
    *,
    name: str,
    rule: str,
    sample_size: int,
) -> CheckResult:
    """Conta divergências e guarda somente uma amostra segura para o relatório."""
    issue_count = dataframe.count()
    sample = [
        _row_to_dict(row)
        for row in dataframe.limit(sample_size).collect()
    ]
    status = "passed" if issue_count == 0 else "failed"
    message = (
        "Nenhuma divergência encontrada."
        if issue_count == 0
        else f"{issue_count} divergência(s) encontrada(s)."
    )
    return CheckResult(name, rule, status, issue_count, message, sample)


def run_validation(config: dict[str, Any]) -> ValidationReport:
    """Executa regras legadas e regras configuráveis na mesma execução."""
    migration_name = config.get("migration", {}).get("name", "validation")
    sample_size = int(config.get("report", {}).get("sample_size", 20))
    report = ValidationReport(migration_name, datetime.now())
    source_config = config["source"]
    target_config = config["target"]
    jars = collect_jars(source_config, target_config)
    spark = create_spark_session(jars)
    spark.sparkContext.setLogLevel("ERROR")

    try:
        datasets = {
            "source": read_dataset(spark, source_config),
            "target": read_dataset(spark, target_config),
        }
        source = datasets["source"]
        target = datasets["target"]
        key = config["key"]
        checks_config = config["checks"]

        if checks_config.get("duplicate_keys", False):
            report.results.append(
                _evaluate(
                    find_duplicate_keys(target, key),
                    name="Chaves duplicadas",
                    rule="duplicate_keys",
                    sample_size=sample_size,
                )
            )
        if checks_config.get("missing_records", False):
            report.results.append(
                _evaluate(
                    find_missing_records(source, target, key),
                    name="Registros ausentes no destino",
                    rule="missing_records",
                    sample_size=sample_size,
                )
            )
        for column in checks_config.get("compare_columns", []):
            report.results.append(
                _evaluate(
                    find_value_differences(source, target, key, column),
                    name=f"Diferenças na coluna {column}",
                    rule="value_differences",
                    sample_size=sample_size,
                )
            )
        for rule_config in checks_config.get("rules", []):
            report.results.append(
                _evaluate(
                    execute_rule(rule_config, datasets),
                    name=rule_config.get("name", rule_config["rule"]),
                    rule=rule_config["rule"],
                    sample_size=sample_size,
                )
            )
    finally:
        report.finished_at = datetime.now()
        spark.stop()

    return report


# @hugaojanuario
