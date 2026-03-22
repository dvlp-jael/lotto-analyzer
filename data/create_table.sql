CREATE EXTERNAL TABLE IF NOT EXISTS lotto_db.lotto_numbers (
  round INT,
  num1 INT,
  num2 INT,
  num3 INT,
  num4 INT,
  num5 INT,
  num6 INT,
  bonus INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES ('field.delim' = ',')
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://lotto-analyzer-data/lotto/'
TBLPROPERTIES ('skip.header.line.count' = '1')