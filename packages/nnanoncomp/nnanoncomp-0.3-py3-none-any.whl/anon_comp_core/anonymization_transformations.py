from pyspark.sql.functions import sha2, col, current_timestamp, lit, year, DataFrame


class Transformations():
    @staticmethod
    def _salted_sha2(c: col, salt: str = "asd") -> str:
        return sha2(f"{salt}{c.cast(StringType())}", 256)

    @staticmethod
    def salted_hash(df: DataFrame, c: str) -> DataFrame:
        # df = df.withColumn(f"anon_{c}", self._salted_sha2(col(c)))
        df = df.withColumn(f"anon_{c}", sha2(col(c).cast(StringType()), 256))

        return df.drop(c)

    @staticmethod
    def year_only(df: DataFrame, c: str) -> DataFrame:
        df = df.withColumn(f"year_{c}", year(col(c)))
        return df.drop(c)

    @staticmethod
    def bucketing(df: DataFrame, inputCol: str, splits: list, outputCol: str = None, bucket_names: dict = None) -> DataFrame:
        bucketizer = Bucketizer(
            splits=splits,
            inputCol=inputCol,
            outputCol=outputCol or f"bucket_{inputCol}"
        )

        bucketed = bucketizer.transform(df)
        bucketed = bucketed.drop(inputCol)

        if bucket_names:
            udf_foo = udf(lambda x: bucket_names[x], StringType())
            
            bucketed = bucketed.withColumn(f"named_bucket_{inputCol}", udf_foo(f"bucket_{inputCol}"))

        return bucketed
