# argparse-types

[![Build, Test and Release Python Package](https://github.com/zegelin/argparse-types/actions/workflows/main.yaml/badge.svg)](https://github.com/zegelin/argparse-types/actions/workflows/main.yaml)

A collection of type converter functions for use with Python's built-in argparse library.

```python
import sys
import argparse
import argtypes.files

parser = argparse.ArgumentParser(prog='example')
parser.add_argument('file', type=argtypes.files.ExistingFile())

args = parser.parse_args(sys.argv)
```

```shell
$ example /some/directory/non-existent-file
example: error: argument file: file "/some/directory/non-existent-file" does not exist.
```

## Paths

These functions return instances of `pathlib.Path`.

Function | Description
--- | ---
`argtypes.paths.ExistingFile()` | Checks if the argument is a path to an existing regular file.<br/><br/>Raises `ArgumentTypeError` if the file doesn't exist, or if the path exists but isn't a regular file.
`argtypes.paths.ExistingDirectory()` | Checks if the argument is a path to an existing directory.<br/><br/>Raises `ArgumentTypeError` if the directory doesn't exist, or if the path exists but isn't a directory.
`argtypes.paths.ExistingMount()` | Checks if the argument is a path to an existing filesystem mount point.<br/><br/>Raises `ArgumentTypeError` if the mount point doesn't exist, or the path exists but isn't a mount point.
`argtypes.paths.ExistingFifo()` | Checks if the argument is a path to an existing FIFO.<br/><br/>Raises `ArgumentTypeError` if the FIFO doesn't exist, or the path exists but isn't a FIFO.
`argtypes.paths.ExistingBlockDevice()` | Checks if the argument is a path to an existing block device.<br/><br/>Raises `ArgumentTypeError` if the block device doesn't exist, or the path exists but isn't a block device.
`argtypes.paths.ExistingCharDevice()` | Checks if the argument is a path to an existing character device.<br/><br/>Raises `ArgumentTypeError` if the character device doesn't exist, or the path exists but isn't a mount point.
`argtypes.paths.ExistingSocket()` | Checks if the argument is a path to an existing socket.<br/><br/>Raises `ArgumentTypeError` if the socket doesn't exist, or the path exists but isn't a socket.
`argtypes.paths.ExistingSymlink()` | Checks if the argument is a path to an existing symlink.<br/><br/>Raises `ArgumentTypeError` if the symlink doesn't exist, or the path exists but isn't a symlink.
`argtypes.paths.NonexistentOrEmptyDirectory()` | Checks if the argument is a path to an empty directory, or a directory that doesn't exist.<br/><br/>Raises `ArgumentTypeError` if the path exists but isn't an empty directory.


## Files

Function | Type | Description
--- | --- | ---
`argtypes.files.YamlFile()` | Any | Checks that the argument is an existing regular file (via `paths.ExistingFile()`), opens it for reading, and loads the contents via PyYAMLs `load` function.<br/><br/>Raises `ArgumentTypeError` if the file doesn't exist, if the path exists but isn't a regular file, or if the file is not valid YAML.
`argtypes.paths.JsonFile()` | Any | Checks that the argument is an existing regular file (via `paths.ExistingFile()`), opens it for reading, and loads the contents via Python's built-in `json.load` function.<br/><br/>Raises `ArgumentTypeError` if the file doesn't exist, if the path exists but isn't a regular file, or if the file is not valid JSON.
