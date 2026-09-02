from typing import Any

from pyspark.sql import DataFrame

from dataqualy.checks import (
    find_invalid_dates,
    find_invalid_pattern,
    find_invalid_values,
    find_null_values,
    find_orphan_records,
    find_suspicious_text,
)


def execute_rule(
    rule_config: dict[str, Any],
    datasets: dict[str, DataFrame],
) -> DataFrame:
    """Traduz uma regra YAML para uma validação Spark."""
    rule = rule_config["rule"]
    dataframe = datasets[rule_config.get("dataset", "target")]

    if rule == "not_null":
        return find_null_values(dataframe, rule_config["columns"])
    if rule == "allowed_values":
        return find_invalid_values(
            dataframe,
            rule_config["column"],
            rule_config["allowed"],
        )
    if rule == "pattern":
        return find_invalid_pattern(
            dataframe,
            rule_config["column"],
            rule_config["pattern"],
        )
    if rule == "valid_date":
        return find_invalid_dates(
            dataframe,
            rule_config["column"],
            rule_config["format"],
        )
    if rule == "no_orphans":
        return find_orphan_records(
            dataframe,
            datasets[rule_config["parent_dataset"]],
            rule_config["child_key"],
            rule_config["parent_key"],
        )
    if rule == "suspicious_text":
        return find_suspicious_text(dataframe, rule_config["columns"])

    raise ValueError(f"Regra não suportada: {rule}")


# @hugaojanuario
