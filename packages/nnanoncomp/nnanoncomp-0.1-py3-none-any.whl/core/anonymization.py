from pyspark.sql.streaming import StreamingQuery
from pyspark.sql.types import StructType, StringType
from pyspark.sql import SparkSession

from pyspark.ml.feature import Bucketizer

from anonymization_transformations import Transformations

class BaseTable():
    def __init__(
        self,
        data_path: str,
        legal_table_name: str,
        checkpoint_path: str,
        schema: StructType = None
        ):
        self.data_path = data_path
        self.legal_table_name = legal_table_name
        self.schema = schema
        self.checkpoint_path = checkpoint_path
        self.spark = SparkSession.builder.getOrCreate()
    
    def _read_stream(self):
        return (
            self.spark.readStream.format('delta').load(self.data_path)
        )


class LegalProcessor(BaseTable, Transformations):
    def __init__(
        self,  
        data_path: str, 
        legal_table_name: str,
        actions: dict,
        # spark,
        checkpoint_path: str, 
        schema: StructType = None
    ):
        super().__init__(data_path=data_path, legal_table_name=legal_table_name, checkpoint_path=checkpoint_path, schema=schema)
        self.actions = actions

    def run_process(self) -> None:
        streamDF = self._read_stream()

        for key, values in self.actions.items():
            for value in values:
                streamDF = getattr(self, key)(streamDF, **value)

        stream_query = (streamDF
            .withColumn("updated", current_timestamp())
            .withColumn("state", lit("inserted"))
            .writeStream
            .option("checkpointLocation", f"{self.checkpoint_path}/{self.legal_table_name}")
            .trigger(once=True)
            .toTable(f"{self.legal_table_name}")
        )

        stream_query.awaitTermination()
