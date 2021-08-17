import argparse
import tempfile
from pathlib import Path
from unittest import TestCase

import yaml

from argtypes.files import YamlFile


class TestYamlFile(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_yaml_file(self):
        p = Path(self.temp_dir.name) / 'valid.yaml'
        data = {'hello': 'world'}

        with p.open('w') as f:
            yaml.dump(data, f)

        self.assertDictEqual(YamlFile()(p), data)

    def test_invalid_yamlfile(self):
        p = Path(self.temp_dir.name) / 'invalid.yaml'

        with p.open('wb') as f:
            f.write(b'\x00l\x00o\x00l')

        with self.assertRaises(argparse.ArgumentTypeError):
            YamlFile()(p)

