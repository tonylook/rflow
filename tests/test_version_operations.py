import unittest
import tempfile
from unittest.mock import MagicMock
import json
import os

import click

from rflow.version_operations import (read_current_version, read_next_version, increment_major_version,
                                      increment_minor_version, increment_patch_version, check_version_info_exists,
                                      init_version, get_latest_release_version)


class TestVersionOperations(unittest.TestCase):
    def setUp(self):
        self.version_info = {
            'currentVersion': '1.0.0',
            'nextVersion': '1.0.1',
        }
        self.temp_dir = tempfile.TemporaryDirectory()
        self.version_file = os.path.join(self.temp_dir.name, 'version.info')
        with open(self.version_file, 'w') as f:
            json.dump(self.version_info, f)

        os.chdir(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_read_current_version(self):
        self.assertEqual(read_current_version(), '1.0.0')

    def test_read_next_version(self):
        self.assertEqual(read_next_version(), '1.0.1')

    def test_increment_major_version(self):
        self.assertEqual(increment_major_version('1.2.3'), '2.0.0')

    def test_increment_minor_version(self):
        self.assertEqual(increment_minor_version('1.2.3'), '1.3.0')

    def test_increment_patch_version(self):
        self.assertEqual(increment_patch_version('1.2.3'), '1.2.4')

    def test_check_version_info_exists(self):
        self.tearDown()
        with self.assertRaises(click.Abort):
            check_version_info_exists()

    def test_init_version(self):
        self.assertEqual(init_version(), '1.0.0')

    def test_get_latest_release_version(self):
        class FakeBranch:
            def __init__(self, name):
                self.name = name

        fake_repo = MagicMock()
        fake_repo.branches = [
            FakeBranch('release/v1.0.0'),
            FakeBranch('release/v1.2.0'),
            FakeBranch('release/v1.3.0'),
        ]
        self.assertEqual(get_latest_release_version(fake_repo), '1.3.0')


if __name__ == '__main__':
    unittest.main()
