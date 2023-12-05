from click.testing import CliRunner
from git.exc import GitError

from rflow.main import cli

def test_release_branch_creation_success(mocker):
    # Mock the git.Repo class and its methods
    mocker.patch('git.Repo')
    mocker.patch('git.Repo.git.checkout')
    mocker.patch('git.Repo.git.push')

    runner = CliRunner()
    result = runner.invoke(cli, ['release', '--version', '1.0.1'])

    assert result.exit_code == 0
    assert "Release branch release/v1.0.1 created and pushed." in result.output

def test_release_branch_creation_failure(mocker):
    # Mock the git.Repo class to raise a GitError
    mocker.patch('git.Repo', side_effect=GitError("git error"))

    runner = CliRunner()
    result = runner.invoke(cli, ['release', '--version', '1.0.1'])

    assert result.exit_code == 0
    assert "Error: git error" in result.output

