import unittest
from unittest.mock import patch

from rflow.git_operations import (is_release_branch, get_main_branch_name)


class TestGitOperations(unittest.TestCase):
    def test_is_release_branch(self):
        self.assertTrue(is_release_branch('release/v1.0.0'))
        self.assertFalse(is_release_branch('main'))

    @patch('rflow.git_operations.git.Repo', autospec=True)
    def test_get_main_branch_name(self, mock_repo):
        mock_repo.branches = ['main']
        self.assertEqual(get_main_branch_name(mock_repo), 'main')

        mock_repo.branches = ['master']
        self.assertEqual(get_main_branch_name(mock_repo), 'master')

        mock_repo.branches = ['fail']
        with self.assertRaises(ValueError):
            get_main_branch_name(mock_repo)


if __name__ == '__main__':
    unittest.main()
