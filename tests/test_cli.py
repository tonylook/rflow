import unittest
from click.testing import CliRunner
from unittest.mock import patch

from rflow.cli import (version, cli)


class TestCli(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    @patch('rflow.cli.git_operations')
    @patch('rflow.cli.version_operations')
    def test_version(self, mock_version_operations):
        mock_version_operations.read_current_version.return_value = '1.0.0'
        result = self.runner.invoke(version)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Current version: 1.0.0", result.output)

    @patch('rflow.cli.git_operations')
    def test_cli(self):
        result = self.runner.invoke(cli)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("rflow: try 'rflow --help' for more information", result.output)


if __name__ == "__main__":
    unittest.main()
