#!/usr/bin/python3
'Utility to fetch and add current ASX prices to one or more gnucash files.'
# Author: Mark Blakeney, Jan 2020.

import os
import sys
import argparse
import gzip
import re
import requests
from pathlib import Path
from datetime import datetime
from fractions import Fraction

URL = 'https://www.asx.com.au/asx/1/share/{}'
PROGNAME = Path(sys.argv[0]).name
LOCKEXT = '.LCK'

TEMPLATE = '''
  <price>
    <price:commodity>
      <cmdty:space>ASX</cmdty:space>
      <cmdty:id>{code}</cmdty:id>
    </price:commodity>
    <price:currency>
      <cmdty:space>CURRENCY</cmdty:space>
      <cmdty:id>AUD</cmdty:id>
    </price:currency>
    <price:time>
      <ts:date>{dt}</ts:date>
    </price:time>
    <price:source>Finance::Quote</price:source>
    <price:type>last</price:type>
    <price:value>{price}</price:value>
  </price>
'''.lstrip('\n')

temp = TEMPLATE.splitlines()
match_start = temp[0]
match_code = temp[2]
match_end = temp[-1]

sess = requests.Session()
now = None
cache = {}

def getprice(args, path, code):
    'Get price for given code and return template'
    price, pricef = cache.get(code, (None, None))
    if price is None:
        r = sess.get(URL.format(code))
        if r.status_code != requests.codes.ok:
            print(f'Fetch error for {code}', file=sys.stderr)
            return None
        price = r.json().get('last_price', 0)
        pricef = str(Fraction(price).limit_denominator())
        cache[code] = (price, pricef)

    if not args.quiet:
        print(f'Fetched {code:4} @ ${price} ({pricef}) for {path.name}')

    return TEMPLATE.format(code=code, dt=now, price=pricef)

def process(args, path, fin, fout):
    'Process the given input to the given output'
    buffer = []
    next_code = False
    codes = set()
    changed = False
    for line in fin:
        line = line.rstrip()
        if line == match_start:
            buffer.append(line + '\n')
        elif not buffer:
            fout.write(line + '\n')
        else:
            buffer.append(line + '\n')
            if next_code:
                code = re.sub(r'^.*>(.+?)<.*$', r'\1', line)
                if code not in codes:
                    res = getprice(args, path, code)
                    if res:
                        fout.writelines(res)
                        changed = True
                    codes.add(code)
                next_code = False
            elif line == match_end:
                fout.writelines(buffer)
                buffer = []
            elif line == match_code:
                next_code = True

    return changed

def process_file(args, path):
    'Process given file'
    lockfile = path.with_name(path.name + LOCKEXT)
    if lockfile.exists():
        if args.ignore_open:
            return True

        print(f'Error: {path} is in use.', file=sys.stderr)
        return False

    compressed = True
    fin = gzip.open(path, 'rt')
    try:
        fin.read(1)
    except OSError:
        fin = open(path, 'rt')
        compressed = False
    else:
        fin.seek(0)

    if args.dry_run:
        pathout = None
        fout = open(os.devnull, 'wt')
    else:
        pathout = path.with_name(f'.{PROGNAME}-{path.name}')
        fout = gzip.open(pathout, 'wt') if compressed else pathout.open('wt')

    changed = process(args, path, fin, fout)

    fin.close()
    fout.close()

    if pathout:
        if changed:
            pathout.replace(path)
        else:
            pathout.unlink()

    return True

def process_path(args, path):
    'Process given path (file, or dir of files)'
    if not path.exists():
        print(f'{path} does not exist', file=sys.stderr)
        return False

    if path.is_dir():
        nofile = True
        allok = True
        for f in path.glob('./*.gnucash'):
            if not f.is_dir() and not f.name.startswith(f'.{PROGNAME}') and \
                    '.gnucash.' not in f.name:
                nofile = False
                if not process_file(args, f):
                    allok = False

        if allok and nofile:
            print('No gnucash files found', file=sys.stderr)
            allok = False
    else:
        allok = process_file(args, path)

    return allok

def main():
    'Main code'
    global now
    # Process command line options
    opt = argparse.ArgumentParser(description=__doc__.strip())
    opt.add_argument('-i', '--ignore-open', action='store_true',
            help='silently ignore any files currently open')
    opt.add_argument('-q', '--quiet', action='store_true',
            help='suppress message output')
    opt.add_argument('-d', '--dry-run', action='store_true',
            help='do not update any file[s]')
    opt.add_argument('path', nargs='+',
            help='directories or files to update')
    args = opt.parse_args()

    now = datetime.now().astimezone().isoformat(sep=' ',
            timespec='seconds').replace('+', ' +')

    error = False
    for path in args.path:
        if not process_path(args, Path(path)):
            error = True

    return 1 if error else 0

if __name__ == '__main__':
    sys.exit(main())
