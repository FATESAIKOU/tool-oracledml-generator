-- DDL for all Oracle column types (常用型別)
CREATE TABLE all_types_table (
  col_number NUMBER,
  col_float FLOAT,
  col_binary_float BINARY_FLOAT,
  col_binary_double BINARY_DOUBLE,
  col_char CHAR(10),
  col_varchar2 VARCHAR2(50),
  col_nchar NCHAR(10),
  col_nvarchar2 NVARCHAR2(50),
  col_date DATE,
  col_timestamp TIMESTAMP,
  col_timestamp_tz TIMESTAMP WITH TIME ZONE,
  col_timestamp_ltz TIMESTAMP WITH LOCAL TIME ZONE,
  col_clob CLOB,
  col_nclob NCLOB,
  col_blob BLOB,
  col_raw RAW(16),
  col_long LONG,
  col_rowid ROWID,
  col_urowid UROWID
);
