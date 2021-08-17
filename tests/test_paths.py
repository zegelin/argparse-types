import argparse
import os
import platform
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import TestCase

from argtypes.paths import ExistingFile, NonexistentOrEmptyDirectory, ExistingDirectory, ExistingMount, ExistingFifo, \
    ExistingBlockDevice, ExistingCharDevice, ExistingSocket, ExistingSymlink

NONEXISTENT_RE = '.* does not exist'
WRONG_TYPE_RE = '.* is not a .*'

class PathTestBase(TestCase):
    def setUp(self):
        dir = tempfile.TemporaryDirectory()
        self.temp_dir = Path(dir.name)
        self.tearDown = dir.cleanup


class TestExistingFile(PathTestBase):
    def test_existing_file(self):
        p = self.temp_dir / 'file'
        p.touch()

        self.assertEqual(ExistingFile()(str(p)), p)  # test str -> Path
        self.assertEqual(ExistingFile()(p), p)

    def test_nonexistent_file(self):
        p = self.temp_dir / 'nonexistent-file'

        with self.assertRaisesRegex(argparse.ArgumentTypeError, NONEXISTENT_RE):
            ExistingFile()(p)

    def test_directory_not_file(self):
        with self.assertRaisesRegex(argparse.ArgumentTypeError, WRONG_TYPE_RE):
            ExistingFile()(self.temp_dir)


class TestExistingDirectory(PathTestBase):
    def test_existing_directory(self):
        p = self.temp_dir

        self.assertEqual(ExistingDirectory()(str(p)), p)  # test str -> Path
        self.assertEqual(ExistingDirectory()(p), p)

    def test_nonexistent_directory(self):
        p = self.temp_dir / 'nonexistent-directory'

        with self.assertRaisesRegex(argparse.ArgumentTypeError, NONEXISTENT_RE):
            ExistingDirectory()(p)

    def test_file_not_directory(self):
        p = self.temp_dir / 'file'
        p.touch()

        with self.assertRaisesRegex(argparse.ArgumentTypeError, WRONG_TYPE_RE):
            ExistingDirectory()(p)


@unittest.skipIf(sys.version_info[0:2] < (3, 7), "Path.is_mount added in 3.7")
class TestExistingMount(PathTestBase):
    def test_existing_mount(self):
        p = Path('/')  # TODO: win32 and other non-posix platforms

        self.assertEqual(ExistingMount()(str(p)), p)  # test str -> Path
        self.assertEqual(ExistingMount()(p), p)

    def test_nonexistent_mount(self):
        p = self.temp_dir / 'nonexistent-mount'

        with self.assertRaisesRegex(argparse.ArgumentTypeError, NONEXISTENT_RE):
            ExistingMount()(p)

    def test_file_not_mount(self):
        p = self.temp_dir / 'file'
        p.touch()

        with self.assertRaisesRegex(argparse.ArgumentTypeError, WRONG_TYPE_RE):
            ExistingMount()(p)


class TestExistingFifo(PathTestBase):
    def test_existing_fifo(self):
        p = self.temp_dir / 'fifo'
        os.mkfifo(p)

        self.assertEqual(ExistingFifo()(str(p)), p)  # test str -> Path
        self.assertEqual(ExistingFifo()(p), p)

    def test_nonexistent_fifo(self):
        p = self.temp_dir / 'nonexistent-fifo'

        with self.assertRaisesRegex(argparse.ArgumentTypeError, NONEXISTENT_RE):
            ExistingFifo()(p)

    def test_file_not_fifo(self):
        p = self.temp_dir / 'file'
        p.touch()

        with self.assertRaisesRegex(argparse.ArgumentTypeError, WRONG_TYPE_RE):
            ExistingFifo()(p)


class TestExistingBlockDevice(PathTestBase):
    pass  # TODO: what is a good platform-agnostic way to find an existing blockdev to test against?


class TestExistingCharDevice(PathTestBase):
    def test_existing_char_device(self):
        p = Path('/dev/zero')

        self.assertEqual(ExistingCharDevice()(str(p)), p)  # test str -> Path
        self.assertEqual(ExistingCharDevice()(p), p)

    def test_nonexistent_char_device(self):
        p = self.temp_dir / 'nonexistent-chardev'

        with self.assertRaisesRegex(argparse.ArgumentTypeError, NONEXISTENT_RE):
            ExistingCharDevice()(p)

    def test_file_not_char_device(self):
        p = self.temp_dir / 'file'
        p.touch()

        with self.assertRaisesRegex(argparse.ArgumentTypeError, WRONG_TYPE_RE):
            ExistingCharDevice()(p)


class TestExistingSocket(PathTestBase):
    def test_existing_socket(self):
        p = self.temp_dir / 'socket'

        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.bind(str(p))

            self.assertEqual(ExistingSocket()(str(p)), p)  # test str -> Path
            self.assertEqual(ExistingSocket()(p), p)

    def test_nonexistent_socket(self):
        p = self.temp_dir / 'nonexistent-socket'

        with self.assertRaisesRegex(argparse.ArgumentTypeError, NONEXISTENT_RE):
            ExistingSocket()(p)

    def test_file_not_socket(self):
        p = self.temp_dir / 'file'
        p.touch()

        with self.assertRaisesRegex(argparse.ArgumentTypeError, WRONG_TYPE_RE):
            ExistingSocket()(p)


class TestExistingSymlink(PathTestBase):
    def test_existing_socket(self):
        p = self.temp_dir / 'symlink'
        p.symlink_to(p / 'file')

        self.assertEqual(ExistingSymlink()(str(p)), p)  # test str -> Path
        self.assertEqual(ExistingSymlink()(p), p)

    def test_nonexistent_socket(self):
        p = self.temp_dir / 'nonexistent-symlink'

        with self.assertRaisesRegex(argparse.ArgumentTypeError, NONEXISTENT_RE):
            ExistingSymlink()(p)

    def test_file_not_socket(self):
        p = self.temp_dir / 'file'
        p.touch()

        with self.assertRaisesRegex(argparse.ArgumentTypeError, WRONG_TYPE_RE):
            ExistingSymlink()(p)


class TestNonexistentOrEmptyDirectory(PathTestBase):
    def test_nonexistent_directory(self):
        p = self.temp_dir / 'nonexistent-directory'

        self.assertEqual(NonexistentOrEmptyDirectory()(str(p)), p)  # test str -> Path
        self.assertEqual(NonexistentOrEmptyDirectory()(p), p)

    def test_existing_empty_directory(self):
        p = self.temp_dir / 'empty-dir'
        p.mkdir()

        self.assertEqual(NonexistentOrEmptyDirectory()(str(p)), p)  # test str -> Path
        self.assertEqual(NonexistentOrEmptyDirectory()(p), p)  # test str -> Path

    def test_file_not_directory(self):
        p = self.temp_dir / 'file'
        p.touch()

        with self.assertRaisesRegex(argparse.ArgumentTypeError, '.* must be a directory.'):
            NonexistentOrEmptyDirectory()(p)

    def test_existing_nonempty_directory(self):
        p = self.temp_dir / 'nonempty-dir'
        p.mkdir()
        (p / 'file').touch()

        with self.assertRaisesRegex(argparse.ArgumentTypeError, '.* must be an empty directory.'):
            NonexistentOrEmptyDirectory()(p)

