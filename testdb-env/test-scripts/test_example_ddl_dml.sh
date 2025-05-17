#!/bin/bash

CONTAINER_NAME="oracle12c-test"
ORACLE_USER="testuser"
ORACLE_PWD="testpwd"
ORACLE_CONN="//localhost:1521/FREEPDB1"
TABLE_NAME="TEST_TABLE"

TESTCMD=$(cat <<EOF
echo "SELECT "'*'" FROM ${TABLE_NAME};" | sqlplus -L ${ORACLE_USER}/${ORACLE_PWD}@${ORACLE_CONN}
EOF
)

docker exec $CONTAINER_NAME bash -c "$TESTCMD"