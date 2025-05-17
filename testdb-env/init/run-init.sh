#!/bin/bash
# Run all DDL and DML scripts in the correct order

set -ex

PDB_NAME="FREEPDB1"
ORACLE_CONN="//localhost:1521/$PDB_NAME"
SYS_CONN="sys/oracle@//localhost:1521/$PDB_NAME as sysdba"
APP_USER="testuser"
APP_PWD="testpwd"

# Wait for Oracle to be ready (用 sysdba 等待)
until echo "exit" | sqlplus -L $SYS_CONN; do
  echo "Waiting for Oracle to be available (sysdba)..."
  sleep 5
done

echo "Creating and granting user if needed..."
echo "ALTER SESSION SET \"_ORACLE_SCRIPT\"=true;" | sqlplus -L $SYS_CONN
(echo "CREATE USER $APP_USER IDENTIFIED BY $APP_PWD;"; echo "GRANT CONNECT, RESOURCE, DBA TO $APP_USER;"; echo "ALTER USER $APP_USER QUOTA UNLIMITED ON USERS;") | sqlplus -L $SYS_CONN || true

# Wait for APP_USER to be ready
until echo "exit" | sqlplus -L $APP_USER/$APP_PWD@$ORACLE_CONN; do
  echo "Waiting for Oracle to be available (app user)..."
  sleep 5
done

echo "Oracle is up. Running DDL scripts..."
for f in /opt/oracle/scripts/ddl/*.sql; do
  echo "Running $f"
  sqlplus -L $APP_USER/$APP_PWD@$ORACLE_CONN @"$f"
done

echo "Running DML scripts..."
for f in /opt/oracle/scripts/dml/*.sql; do
  echo "Running $f"
  sqlplus -L $APP_USER/$APP_PWD@$ORACLE_CONN @"$f"
done

echo "All scripts executed."
