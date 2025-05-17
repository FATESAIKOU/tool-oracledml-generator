#!/usr/bin/env python
import json
import random
import string
import sys
from datetime import datetime, timedelta
import base64

def random_int(min_v, max_v):
    return random.randint(min_v, max_v)

def random_float(min_v, max_v, precision):
    value = random.uniform(min_v, max_v)
    return round(value, precision)

def random_str(pattern):
    # Support pattern: [abcdefg]*n[_]*1[xyz]*n and direct string
    import re
    result = ''
    regex = re.compile(r'\[([^\]]+)\]\*([0-9]+)')
    pos = 0
    for m in regex.finditer(pattern):
        start, end = m.span()
        # Add direct string part before pattern
        if start > pos:
            result += pattern[pos:start]
        chars, count = m.group(1), int(m.group(2))
        result += ''.join(random.choices(chars, k=count))
        pos = end
    # Add last direct string part
    if pos < len(pattern):
        result += pattern[pos:]
    # If pattern has no []*n, return as is
    if not regex.search(pattern):
        return pattern
    return result

def random_date():
    start = datetime(2000, 1, 1)
    end = datetime(2030, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')

def random_timestamp():
    start = datetime(2000, 1, 1)
    end = datetime(2030, 12, 31)
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return (start + timedelta(seconds=random_seconds)).strftime('%Y-%m-%d %H:%M:%S')

def random_blob(length=8):
    return base64.b16encode(random.randbytes(length)).decode('ascii')

def random_raw(length=8):
    return base64.b16encode(random.randbytes(length)).decode('ascii')

def random_rowid():
    # Simulate a valid ROWID format (not guaranteed to be accepted by Oracle)
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=18))

def main():
    if len(sys.argv) < 2:
        print('Usage: python gen_random_dml.py <rule.json>')
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        rules = json.load(f)
    username = rules['username']
    tablename = rules['tablename']
    columns = []
    values = []
    for col, rule in rules.items():
        if col in ['username', 'tablename']:
            continue
        if 'min' in rule and 'max' in rule and 'decimal_places' not in rule:
            v = random_int(rule['min'], rule['max'])
            values.append(str(v))
            columns.append(col)
        elif 'min' in rule and 'max' in rule and 'decimal_places' in rule:
            v = random_float(rule['min'], rule['max'], rule['decimal_places'])
            values.append(str(v))
            columns.append(col)
        elif 'pattern' in rule:
            v = random_str(rule['pattern'])
            values.append(f"'{v}'")
            columns.append(col)
        elif rule.get('type') == 'date':
            if 'value' in rule:
                # Support YYYY/MM/DD HH:mm:ss
                dt = rule['value']
                # Oracle DATE only supports up to seconds
                values.append(f"TO_DATE('{dt}','YYYY/MM/DD HH24:MI:SS')")
            else:
                v = random_date()
                values.append(f"TO_DATE('{v}','YYYY-MM-DD')")
            columns.append(col)
        elif rule.get('type') == 'timestamp':
            if 'value' in rule:
                dt = rule['value']
                values.append(f"TO_TIMESTAMP('{dt}','YYYY/MM/DD HH24:MI:SS')")
            else:
                v = random_timestamp()
                values.append(f"TO_TIMESTAMP('{v}','YYYY-MM-DD HH24:MI:SS')")
            columns.append(col)
        elif rule.get('type') == 'blob':
            v = random_blob()
            values.append(f"HEXTORAW('{v}')")
            columns.append(col)
        elif rule.get('type') == 'raw':
            v = random_raw()
            values.append(f"HEXTORAW('{v}')")
            columns.append(col)
        elif rule.get('type') == 'rowid':
            v = random_rowid()
            values.append(f"'{v}'")
            columns.append(col)
        else:
            values.append('NULL')
            columns.append(col)
    # Pretty print SQL
    indent = '    '
    col_lines = ',\n'.join([indent + c for c in columns])
    val_lines = ',\n'.join([indent + v for v in values])
    sql = f"INSERT INTO {username}.{tablename} (\n{col_lines}\n) VALUES (\n{val_lines}\n);"
    print(sql)

if __name__ == '__main__':
    main()
