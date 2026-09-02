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
    return CheckResult(
        name=name,
        rule=rule,
        status=status,
        issue_count=issue_count,
        message=message,
        sample=sample,
    )


def run_validation(config: dict[str, Any]) -> ValidationReport:
    """Executa as validações definidas na configuração."""
    migration_name = config.get("migration", {}).get("name", "validation")
    sample_size = int(config.get("report", {}).get("sample_size", 20))
    report = ValidationReport(
        migration_name=migration_name,
        started_at=datetime.now(),
    )
    jars = collect_jars(config["source"], config["target"])
    spark = create_spark_session(jars)
    spark.sparkContext.setLogLevel("ERROR")

    try:
        source = read_dataset(spark, config["source"])
        target = read_dataset(spark, config["target"])
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
    finally:
        report.finished_at = datetime.now()
        spark.stop()

    return report


# @hugaojanuario
