CREATE EXTERNAL TABLE IF NOT EXISTS test_db.test_table (
  COL1 integer,
  COL2 timestamp
)
PARTITIONED BY (
  COL3 string,
  COL4 string
)
ROW FORMAT SERDE
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
LOCATION
  's3://test-bucket/test_prefix'
TBLPROPERTIES (
  'classification' = 'parquet',
  'compressionType' = 'snappy',
  'projection.enabled' = 'TRUE',
  'projection.COL3.format' = 'yyyy-MM-dd',
  'projection.COL3.interval' = '1',
  'projection.COL3.interval.unit' = 'DAYS',
  'projection.COL3.range' = 'NOW-2YEARS,NOW',
  'projection.COL3.type' = 'date',
  'projection.COL4.values' = 'VAL1,VAL2',
  'projection.COL4.type' = 'enum'
)
