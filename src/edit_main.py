#!/usr/bin/env python3
"""Edit main.cpp safely: UTF-16LE+BOM+CRLF roundtrip (D285 三连坑的固化修复)."""
import sys
path = sys.argv[1] if len(sys.argv) > 1 else 'main.cpp'
raw = open(path, 'rb').read()
assert raw[:2] == b'\xff\xfe', 'input must start with BOM'
text = raw[2:].decode('utf-16-le')
print(f'loaded {len(text)} chars, first 40: {text[:40]!r}')
mode = sys.argv[2] if len(sys.argv) > 2 else 'check'
if mode == 'save':
    new = sys.stdin.read()
    new = new.replace('\ufeff', '').lstrip('\r\n')
    open(path, 'wb').write(b'\xff\xfe' + new.encode('utf-16-le'))
    chk = open(path, 'rb').read()
    assert chk[:2] == b'\xff\xfe' and b'\xff\xfe' not in chk[2:2+2]
    print(f'saved {len(new)} chars, head hex {chk[:8].hex()}')
