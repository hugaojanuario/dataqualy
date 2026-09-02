import os
import sys
from pathlib import Path

import pyspark

from pyspark.sql import SparkSession #entrada principal do Spark.

def create_spark_session() -> SparkSession:
    os.environ.setdefault(
        "SPARK_HOME",
        str(Path(pyspark.__file__).parent)
    )
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", sys.executable)

    return (
        SparkSession.builder
        .master("local[*]") #usa os núcleus disponíveis do PC.
        .appName("dataqualy") #identifica a aplicação.
        .getOrCreate() #cria ou reutiliza uma sessão.
    )
