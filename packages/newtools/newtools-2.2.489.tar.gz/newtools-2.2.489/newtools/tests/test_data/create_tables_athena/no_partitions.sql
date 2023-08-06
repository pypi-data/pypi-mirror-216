CREATE EXTERNAL TABLE IF NOT EXISTS test_db.test_table (
  COL1 string,
  COL2 timestamp,
  COL3 boolean
)

ROW FORMAT SERDE
  'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION
  's3://test-bucket/test_prefix'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
)
