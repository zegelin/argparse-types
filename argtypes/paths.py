import argparse
import functools
import os.path
from pathlib import Path
from typing import Union, Callable

StrOrPathT = Union[str, Path]
HandlerT = Callable[[StrOrPathT], Path]

def _Existing(typename: str, type_test: Callable[[Path], bool], exists_test: Callable[[Path], bool] = Path.exists, extended_typename: str=None) -> HandlerT:
    extended_typename = typename if extended_typename is None else extended_typename

    def handler(path: StrOrPathT) -> Path:
        path = Path(path)

        if not exists_test(path):
            raise argparse.ArgumentTypeError(f'{typename} "{path}" does not exist.')

        if not type_test(path):
            raise argparse.ArgumentTypeError(f'"{path}" is not a {extended_typename}.')

        return path

    return handler

def ExistingFile() -> HandlerT:
    """
    Returns a Callable that checks if the argument is a path to an existing regular file.

    Raises `ArgumentTypeError` if the file doesn't exist, or if the path exists but isn't a regular file.
    """
    return _Existing('file', Path.is_file, extended_typename='regular file')

def ExistingDirectory() -> HandlerT:
    return _Existing('directory', Path.is_dir)

def ExistingMount() -> HandlerT:
    return _Existing('mount point', Path.is_mount)

def ExistingFifo() -> HandlerT:
    return _Existing('FIFO', Path.is_fifo)

def ExistingBlockDevice() -> HandlerT:
    return _Existing('block device', Path.is_block_device)

def ExistingCharDevice() -> HandlerT:
    return _Existing('char device', Path.is_char_device)

def ExistingSocket() -> HandlerT:
    return _Existing('socket', Path.is_socket)

def ExistingSymlink() -> HandlerT:
    return _Existing('symbolic link', Path.is_symlink, exists_test=os.path.lexists)

def NonexistentOrEmptyDirectory() -> HandlerT:
    def handler(path: StrOrPathT) -> Path:
        path = Path(path)

        if path.exists():
            if not path.is_dir():
                raise argparse.ArgumentTypeError(f'"{path}" must be a directory.')

            if next(path.iterdir(), None) is not None:
                raise argparse.ArgumentTypeError(f'"{path}" must be an empty directory.')

        return path

    return handler
