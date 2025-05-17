#!/bin/bash
# This script connects to the Oracle DB and runs a SELECT statement to verify data

ORACLE_USER="testuser"
ORACLE_PWD="testpwd"
ORACLE_CONN="//localhost:1521/XEPDB1"

# Wait for Oracle to be ready
until echo "exit" | sqlplus -L $ORACLE_USER/$ORACLE_PWD@$ORACLE_CONN; do
  echo "Waiting for Oracle to be available..."
  sleep 5
done

echo "Selecting data from test_table:"
echo "SELECT * FROM test_table;" | sqlplus -L $ORACLE_USER/$ORACLE_PWD@$ORACLE_CONN
