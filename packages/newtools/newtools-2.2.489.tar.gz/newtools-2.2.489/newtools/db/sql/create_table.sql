CREATE EXTERNAL TABLE IF NOT EXISTS {database_name}.{table_name} (
  {columns}
)
{partitioned_by}
ROW FORMAT SERDE
  '{row_format_serde}'
LOCATION
  '{external_location}'
TBLPROPERTIES (
  {tbl_properties}
)
