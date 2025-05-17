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
    # 支援 pattern: [abcdefg]*n[_]*1[xyz]*n
    import re
    result = ''
    regex = re.compile(r'\[([^\]]+)\]\*([0-9]+)')
    matches = list(regex.finditer(pattern))
    for m in matches:
        chars, count = m.group(1), int(m.group(2))
        result += ''.join(random.choices(chars, k=count))
    # 處理 pattern 末尾非 []*n 的部分（完全忽略 length）
    tail = regex.sub('', pattern)
    if tail and not matches:
        # 若 pattern 沒有 []*n，則隨機長度10
        result += ''.join(random.choices(pattern, k=10))
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
    # 模擬一個合法格式
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
        if 'min' in rule and 'max' in rule and '小數點位數' not in rule:
            # 整數
            v = random_int(rule['min'], rule['max'])
            values.append(str(v))
            columns.append(col)
        elif 'min' in rule and 'max' in rule and '小數點位數' in rule:
            # 浮點數
            v = random_float(rule['min'], rule['max'], rule['小數點位數'])
            values.append(str(v))
            columns.append(col)
        elif 'pattern' in rule:
            v = random_str(rule['pattern'])
            values.append(f"'{v}'")
            columns.append(col)
        elif rule.get('type') == 'date':
            v = random_date()
            values.append(f"TO_DATE('{v}','YYYY-MM-DD')")
            columns.append(col)
        elif rule.get('type') == 'timestamp':
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
            # 預設 NULL
            values.append('NULL')
            columns.append(col)
    sql = f"INSERT INTO {username}.{tablename} (" + ', '.join(columns) + ") VALUES (" + ', '.join(values) + ");"
    print(sql)

if __name__ == '__main__':
    main()
