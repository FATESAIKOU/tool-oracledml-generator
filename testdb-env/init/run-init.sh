#!/bin/bash
# Run all DDL and DML scripts in the correct order

set -e

# Wait for Oracle to be ready
until echo "exit" | sqlplus -L testuser/testpwd@//localhost:1521/XEPDB1; do
  echo "Waiting for Oracle to be available..."
  sleep 5
done

echo "Oracle is up. Running DDL scripts..."
for f in /opt/oracle/scripts/ddl/*.sql; do
  echo "Running $f"
  sqlplus -L testuser/testpwd@//localhost:1521/XEPDB1 @"$f"
done

echo "Running DML scripts..."
for f in /opt/oracle/scripts/dml/*.sql; do
  echo "Running $f"
  sqlplus -L testuser/testpwd@//localhost:1521/XEPDB1 @"$f"
done

echo "All scripts executed."
