#!/usr/bin/env python
from __future__ import print_function

import argparse
import re
import sys


def error(s):
    print(s)


def substitute(str_search, str_replace, _input):
    if str_search == '$' and _input[-1] == '\n':
        # Workaround weird Python behavior for `$`.
        # If the "haystack" has a newline (`\n`) at the end, `$` will have TWO
        # matches: one before the `\n` and one after.
        # This is surprising, and impossible to prevent. The only flag
        # affecting this behavior is `re.MULTILINE` which when passed will
        # simply make `$` match before all newlines.
        # This is a small hack to prevent the double matching from `$`.
        #
        # A different possible solution would be to use the '\Z' matching
        # character:
        #
        #     if str_search == '$':
        #         str_search = '\Z'
        #
        # but that replaces _after_ the ending newline, which is not what you
        # want from a good Unix or git-citizen (git best-practice is to have
        # all text files end with a newline).
        #
        # See: https://docs.python.org/3/library/re.html#index-2
        replace_count = 1
        if str_replace.endswith('\\n'):
            # Remove newline at end of pattern
            str_replace = str_replace[:-2]
    else:
        replace_count = 0

    return re.sub(str_search, str_replace, _input, count=replace_count)


def print_match(match, filename=None):
    for line in match.group(0).split('\n'):
        if type(filename) == str:
            print('%s: %s' % (filename, line))
        else:
            print(line)


def print_matching_line(_input, match, filename=None):
    line_start = 0
    # Find line beginning
    for idx in range(match.start(), 0, -1):
        if _input[idx] == '\n':
            line_start = idx + 1
            break
    # Find line end
    for idx in range(match.start(), len(_input)):
        if _input[idx] == '\n':
            line_end = idx
            break

    line = _input[line_start:line_end]
    if type(filename) == str:
        print('%s: %s' % (filename, line))
    else:
        print(line)


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
    parser.add_argument(
        '-c', '--confirm', action='store_true', help='Ask for each replacement'
    )
    parser.add_argument(
        '-g', '--group', help='Print this capture group instead of the whole match'
    )

    args = parser.parse_args()
    is_inplace_replacement = args.in_place
    should_ask = args.confirm

    delimiter = args.regex[0]
    re_prex = re.compile(
        '%s([^%s]+)%s(([^%s]*)%s)?'
        % (delimiter, delimiter, delimiter, delimiter, delimiter)
    )
    matches = re_prex.match(args.regex)
    if not matches:
        error('Unable to understand regex: `%s`' % args.regex)
        exit()

    str_search = matches.group(1)
    str_replace = matches.group(3)

    is_replacing = matches.group(2)

    print_group = None
    if args.group:
        try:
            print_group = int(args.group)
        except ValueError:
            error('-g/--group must be an integer, was "%s"' % args.group)
            exit()

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

        if is_replacing:
            output = ''

            matches = re.finditer(str_search, _input)

            current_pos = 0
            for match in matches:
                output += _input[current_pos : match.start()]

                should_replace = True
                if should_ask:
                    print_matching_line(_input, match, filename)
                    print('Replace? (y/n) ', flush=True, end='')
                    yesno = input()
                    if yesno.lower() not in ('y', 'yes'):
                        should_replace = False

                if should_replace:
                    output += re.sub(str_search, str_replace, match.group(0))
                else:
                    output += match.group(0)

                current_pos = match.end()

            output += _input[current_pos:]

            if is_inplace_replacement:
                with open(filename, 'w') as f:
                    _input = f.write(output)
            else:
                print(output, end='')
        else:
            output = re.finditer(str_search, _input)
            for match in output:
                if print_group:
                    print(match.group(print_group))
                else:
                    for line in match.group(0).split('\n'):
                        if type(filename) == str:
                            print('%s: %s' % (filename, line))
                        else:
                            print(line)


if __name__ == '__main__':
    cmdline_entry_point()
