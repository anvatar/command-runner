# command-runner

For each line from standard input, execute COMMAND and print execution result to standard output.

## Usage

```
usage: command_runner.py [-h] [-i INTERVAL_MS] COMMAND

For each line from standard input, execute COMMAND and print execution result
to standard output.

positional arguments:
  COMMAND               Input will be given through standard input. Standard
                        output and error will be printed to standard error.

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL_MS, --internval-ms INTERVAL_MS
                        (default: 0)
```

## Examples

```bash
$ cat input.txt
This is LINE 1
This is LINE 2

$ command_runner.py -i 500 "tr 'A-Za-z' 'a-zA-Z'" < input.txt > output.txt
Processing <This is LINE 1>
[SUBPROCESS][out] tHIS IS line 1
Processing <This is LINE 2>
[SUBPROCESS][out] tHIS IS line 2

$ cat output.txt
0: This is LINE 1
0: This is LINE 2
```
