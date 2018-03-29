#! /usr/bin/env python2

import sys
import argparse
import command_runner
import os
from subprocess import Popen, PIPE
import shlex
import time


class CommandRunner:
    def __init__(self, file_in, file_out, file_err):
        self._file_in = file_in
        self._file_out = file_out
        self._file_err = file_err

    def run(self, command, interval_in_millis):
        for l in self._file_in:
            line = l.rstrip()
            if line:
                status = self._execute_command_with_line(command, line)
                self._out("{}: {}".format(status, line))

                if interval_in_millis:
                    time.sleep(interval_in_millis / 1000.0)

    def _execute_command_with_line(self, command, line):
        self._err('Processing <' + line + '>')
        popen = Popen(shlex.split(command),
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = popen.communicate(line)
        if stderr:
            for err in stderr.rstrip().split(os.linesep):
                self._err('[SUBPROCESS][err] ' + err.rstrip())
        if stdout:
            for out in stdout.rstrip().split(os.linesep):
                self._err('[SUBPROCESS][out] ' + out.rstrip())
        return popen.returncode

    def _err(self, line):
        self._write_line_and_flush(self._file_err, line)

    def _write_line_and_flush(self, file, line):
        file.write(line)
        file.write(os.linesep)
        file.flush()

    def _out(self, line):
        self._write_line_and_flush(self._file_out, line)


def _main():
    args = _parse_arguments()
    command_runner = CommandRunner(sys.stdin, sys.stdout, sys.stderr)
    command_runner.run(args.command, args.interval_in_millis)


def _parse_arguments():
    description = (
        'For each line from standard input, execute COMMAND and print '
        'execution result to standard output.'
    )
    command_help = (
        'Input will be given through standard input. Standard output and error '
        'will be printed to standard error.'
    )

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('command',
        metavar='COMMAND',
        help=command_help)
    parser.add_argument('-i', '--internval-ms',
        metavar='INTERVAL_MS',
        type=int,
        dest='interval_in_millis',
        default=0,
        help='(default: 0)')
    return parser.parse_args()


if __name__ == '__main__':
    _main()
