"""spark"""

from pandas import DataFrame as PandasDF
from pyspark.sql import DataFrame as SparkDF
from pyspark.sql import SparkSession

from iterable_etl.libs.dbg import dbg


def dataframe_to_spark(df: PandasDF, spark: SparkSession) -> SparkDF:
    """
    Convert the Pandas DataFrame to a Spark DataFrame.

    from pyspark.sql import SparkSession
    spark = SparkSession.builder.getOrCreate()
    """
    spark_df = spark.createDataFrame(df)
    return spark_df


def write_to_databricks_table(spark_df: SparkDF, table_name: str) -> None:
    """
    Write the Spark DataFrame to a Databricks table.
    """
    spark_df.write.mode("overwrite").saveAsTable(table_name)


def write_diff_for_list_user_history(
    spark: SparkSession, pandas_df: PandasDF, target_schema_table_name: str
):
    """
    Write entries to `list_user_history` table WO duplication
    """

    spark_df = spark.createDataFrame(pandas_df)

    spark_df.createOrReplaceTempView("temp_table")

    existing_entries = spark.sql(
        """
        SELECT t1.*
        FROM temp_table t1
        JOIN {} t2 ON t1.list_id = t2.list_id
    """.format(
            target_schema_table_name
        )
    )

    if existing_entries.count() == 0:
        spark_df.write.format("delta").mode("append").saveAsTable(
            target_schema_table_name
        )
    else:
        dbg("Skipping write due to overlapping entries.")
