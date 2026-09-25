#!/usr/bin/env python3

import os
import re
import subprocess
from datetime import datetime
from collections import namedtuple
from argparse import ArgumentParser

BUILD_DIR = './build'

COMMANDS = [
    'bench_cedar',
    'bench_cedarpp',
    'bench_darts',
    'bench_dartsc',
    'bench_dastrie',
    'bench_hattrie',
    'bench_arrayhash',
    'bench_tx',
    'bench_marisa',
    'bench_madras',
    'bench_art',
    '../CoCo-trie-wrapper/build/bench_coco',
    'bench_fst',
    'bench_pdt',
    'bench_xcdat_8',
    'bench_xcdat_16',
    'bench_xcdat_7',
    'bench_xcdat_15',
]


def run_command(cmd):
    print(cmd)
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            encoding='utf-8', shell=True)
    return output.stdout


def main():
    parser = ArgumentParser()
    parser.add_argument('input_keys')
    parser.add_argument('output_json')
    parser.add_argument('-i', '--assume-int', action='store_true',
                         help='pass -i (assume_int) to every engine binary, '
                              'for a numeric-keys input file such as numbers.txt')
    args = parser.parse_args()

    input_keys = args.input_keys
    output_json = args.output_json
    # cmd_line_parser's boolean flags require an explicit value ('-i true'
    # or '-i 1'), not a bare '-i' -- passing a bare flag makes every engine
    # binary print its usage text instead of running.
    extra = ' -i 1' if args.assume_int else ''

    fout = open(output_json, 'wt')
    for command in COMMANDS:
        cmd = f'{BUILD_DIR}/{command} {input_keys}{extra}'
        stdout = run_command(cmd)
        fout.write(stdout)
    fout.close()


if __name__ == "__main__":
    main()
