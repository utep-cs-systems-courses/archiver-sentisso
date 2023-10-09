#! /usr/bin/env python

import sys
from Archiver import Archiver
import os


def print_usage():
    print("Usage:")
    print("   mytar.py c <files to archive...>")
    print("   mytar.py x <file to extract>")


def incorrect_usage():
    print_usage()
    sys.exit(1)


if len(sys.argv) < 3:
    print("Incorrect number of arguments! Exiting...")
    incorrect_usage()

command = sys.argv[1]

archiver = Archiver()

if command == 'c':
    files = sys.argv[2:]

    archiver.archive(files)

elif command == 'x':
    if len(sys.argv) != 3:
        print("Incorrect number of arguments for command x! Exiting...")
        incorrect_usage()

    archive = sys.argv[2]
    if not os.path.exists(archive):
        print("Archive \"%s\" doesn't exist! Exiting..." % archive)
        sys.exit(1)

    archiver.extract(archive)

else:
    print("Unknown command \"%s\"! Exiting..." % command)
    incorrect_usage()
