from pyspark.sql import DataFrame
from pyspark.sql.functions import  col

"""
essa funcao agrupa pela chave e retorna somente os ids repetidos
"""

def find_duplicate_keys(dataframe: DataFrame, key: str) -> DataFrame:
    return (
        dataframe
        .groupBy(key)
        .count()
        .filter(col("count") > 1)
    )

def find_missing_records(source: DataFrame, target: DataFrame, key: str) -> DataFrame:
    """
    Retorna registros da origem que nao existem no destino
    """
    target_keys = target.select(key).dropDuplicates()

    return source.join(target_keys, on=key, how="left_anti")

def find_value_differences(
    source: DataFrame,
    target: DataFrame,
    key: str,
    column: str,
) -> DataFrame:
    """compara uma coluna entre registros com a mesma chave"""
    target_unique = target.dropDuplicates([key])

    joined = source.alias("source").join(
        target_unique.alias("target"),
        col(f"source.{key}") == col(f"target.{key}"),
        how="inner",
    )

    return (
        joined
        .filter(
            ~col(f"source.{column}").eqNullSafe(
                col(f"target.{column}")
            )
        )
        .select(
            col(f"source.{key}").alias(key),
            col(f"source.{column}").alias("source_value"),
            col(f"target.{column}").alias("target_value"),
        )
    )