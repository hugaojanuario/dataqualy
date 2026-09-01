from pyspark.sql import SparkSession #entrada principal do Spark.

def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .master("local[*]") #usa os núcleus disponíveis do PC.
        .appName("dataqualy") #identifica a aplicação.
        .getOrCreate() #cria ou reutiliza uma sessão.
    )