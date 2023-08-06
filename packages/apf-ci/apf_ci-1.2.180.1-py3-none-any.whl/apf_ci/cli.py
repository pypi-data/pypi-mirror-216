#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'LianGuoQing'

import argparse
import pkg_resources

import apf_ci as ci

def _commands(group='apf_ci.commands'):
    commands = pkg_resources.iter_entry_points(group=group)
    return dict((c.name, c) for c in commands)

def dispatch(argv):
    commands = _commands()
    parser = argparse.ArgumentParser(prog=ci.__title__)
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s version {0}".format(ci.__version__),
    )
    parser.add_argument(
        "command",
        choices=commands.keys(),
        help=""
    )
    parser.add_argument(
        "args",
        help=argparse.SUPPRESS,
        nargs=argparse.REMAINDER,
    )

    args = parser.parse_args(argv)

    main = commands[args.command].load()

    main(args.args)