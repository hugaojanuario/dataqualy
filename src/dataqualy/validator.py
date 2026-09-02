from typing import Any

import dataqualy
from dataqualy import checks
from dataqualy.checks import (
    find_duplicate_keys,
    find_missing_records,
    find_value_differences,
)

from dataqualy.reader import read_records

from dataqualy.spark import create_spark_session

def run_validation(config: dict[str, Any]) -> None:
    """executa as validacoes definidas na config"""
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("ERROR")

    try:
        source = read_records(spark, config["source"]["path"])
        target = read_records(spark, config["target"]["path"])
        key = config["key"]
        checks = config["checks"]

        if checks["duplicate_keys"]:
            print("\nChaves duplicadas")
            find_duplicate_keys(target, key).show()

        if checks["missing_records"]
            print("\nRegistros faltantes")
            find_missing_records(source, target, key).show()

        for column in checks["compare_columns"]:
            print(f"\nDiferenças na coluna '{column}'")
            find_value_differences(source, target, key, column).show()
    finally:
        spark.stop()
