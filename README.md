# Oracle 12c Test Environment Guide

## 1. Start Oracle DB

In the `testdb-env/` directory, run:

```sh
docker-compose up -d
```

This will start an Oracle 12c test database and automatically load all SQL files from the `ddl/` and `dml/` directories.

---

## 2. Verify Oracle DB Load Status

Run the following commands to check if tables and data are created correctly:

```sh
./testdb-env/test-scripts/show_all_tbl.sh
```

This script will connect to the database, query all tables, and display their DDL and data.

---

To add new DDL or DML, simply place SQL files into `testdb-env/ddl/` or `testdb-env/dml/` and restart the container to auto-load them.

## 3. Generate & Apply DML

You can generate and inject random DML using:

```sh
./testdb-env/test-scripts/apply_dml.sh <(./gen_random_dml.py all_types_table_rule.json)
```

- Edit `all_types_table_rule.json` to control the generated data.
- The generator supports pattern-based string, date/time, and all Oracle types.
- See comments in the JSON and Python script for details.