CREATE EXTERNAL TABLE IF NOT EXISTS test_input_database.test_table (
  COL1 integer,
  COL2 timestamp
)
PARTITIONED BY (
  COL3 string
)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
LOCATION
  's3://test-bucket/test_prefix'
TBLPROPERTIES (
  'classification' = 'parquet',
  'compressionType' = 'snappy'
)
