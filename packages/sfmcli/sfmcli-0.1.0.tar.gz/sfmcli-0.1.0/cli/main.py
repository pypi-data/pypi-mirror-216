from __future__ import annotations

import argparse
import sys
import textwrap

from cli.handlers import clean_handler
from cli.handlers import config_handler
from cli.handlers import populate_handler


def main() -> int:
    """
    Returns our main CLI
    sfmc cli {-h, -v}
        -h - help message
        -v - cli version'

    sfmc config {new, list, remove}
        new     - set up a new sfmc environment
        list    - list available environments
        remove  - delete a environment

    sfmc populate --origin {origin environment} --target {target environment}
        {origin environment} - name of an existing environment to get data from
        {target environment} - name of an existing environment to insert
    the data

    sfmc clean {environment}
        {environment} - name of an existing environment to clean data
    """
    parser = argparse.ArgumentParser(
        prog='sfmcli',
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='0.1.0',
        help='show the installed cli version',
    )

    sub_parsers = parser.add_subparsers(
        title='available subcommands',
    )

    config_parser = sub_parsers.add_parser(
        'config',
        formatter_class=argparse.RawTextHelpFormatter,
        help='this command help you set up your sfmc environments',
    )
    config_parser.add_argument(
        'action',
        choices=['new', 'list', 'remove'],
        help=textwrap.dedent(
            '''\
        new     - set up a new sfmc environment
        list    - list available environments
        remove  - delete a environment
        ''',
        ),
    )
    config_parser.set_defaults(func=config_handler)

    populate_parser = sub_parsers.add_parser(
        'populate',
        help='populate data extensions in a specified environment',
    )
    populate_parser.add_argument(
        'origin',
        type=str,
        help='name of an existing environment to get data from',
    )
    populate_parser.add_argument(
        'target',
        type=str,
        help='name of an existing environment to insert the data',
    )
    populate_parser.set_defaults(func=populate_handler)

    clean_subparser = sub_parsers.add_parser(
        'clean',
        help=' clear all data exentensions in a specified environment',
    )
    clean_subparser.add_argument(
        'target',
        type=str,
        help='name of an existing environment to cleandata',
    )
    clean_subparser.set_defaults(func=clean_handler)

    args = parser.parse_args(args=(sys.argv[1:] or ['-h']))
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
