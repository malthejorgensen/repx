#!/usr/bin/env python
from __future__ import print_function

import argparse
import re
import sys


RE_PREX = re.compile('/([^/]+)/(([^/]*)/)?')


def error(s):
    print(s)


def cmdline_entry_point():
    parser = argparse.ArgumentParser(
        description='Search and replace in files using regular expressions'
    )
    parser.add_argument(
        'regex',
        type=str,
        action='store',
        help='The regular expression to search and replace with.',
    )
    parser.add_argument(
        'infiles',
        type=str,
        action='store',
        nargs='*',
        help='File to be searched and replaced (if no file is specified \
                              stdin is used',
    )
    parser.add_argument(
        '-i', '--in-place', action='store_true', help='Modify files in-place'
    )

    args = parser.parse_args()
    is_inplace_replacement = args.in_place

    matches = RE_PREX.match(args.regex)
    if not matches:
        error('Unable to understand regex: `%s`' % args.regex)
        exit()

    str_search = matches.group(1)
    str_replace = matches.group(3)

    should_replace = matches.group(2)

    if args.infiles == []:
        infiles = [sys.stdin]
    else:
        infiles = args.infiles

    for filename in infiles:
        if type(filename) == str:
            with open(filename) as f:
                _input = f.read()
        else:
            f = filename
            _input = f.read()

        if should_replace:
            output = re.sub(str_search, str_replace, _input)

            if is_inplace_replacement:
                with open(filename, 'w') as f:
                    _input = f.write(output)
            else:
                print(output, end='')
        else:
            output = re.finditer(str_search, _input)
            for match in output:
                for line in match.group(0).split('\n'):
                    if type(filename) == str:
                        print('%s: %s' % (filename, line))
                    else:
                        print(line)


if __name__ == '__main__':
    cmdline_entry_point()
