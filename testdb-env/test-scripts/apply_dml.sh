#!/bin/bash

CONTAINER_NAME="oracle12c-test"
ORACLE_USER="testuser"
ORACLE_PWD="testpwd"
ORACLE_CONN="//localhost:1521/FREEPDB1"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <sql_file>"
    exit 1
fi

SQL_FILE="$1"
if [ ! -e "$SQL_FILE" ]; then
    echo "File not found: $SQL_FILE"
    exit 2
fi

echo "Applying $SQL_FILE to Oracle..."
docker exec -i $CONTAINER_NAME bash -c "sqlplus -s -L $ORACLE_USER/$ORACLE_PWD@$ORACLE_CONN" < "$SQL_FILE"
