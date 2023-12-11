from unittest.mock import Mock

from click.testing import CliRunner
from git.exc import GitError

from rflow.rflow import cli


def test_release_branch_creation_failure(mocker):
    mocker.patch('git.Repo', side_effect=GitError("git error"))

    runner = CliRunner()
    result = runner.invoke(cli, ['release', '--version', '1.0.1'])

    assert result.exit_code != 0
    assert "Error: git error" in result.output

def test_fix_branch_creation_success(mocker):
    mock_repo = mocker.patch('git.Repo')
    mock_branch = Mock()
    mock_branch.name = 'release/v1.0.1'
    mock_repo.return_value.active_branch = mock_branch

    mocker.patch('git.Repo.git.checkout')
    mocker.patch('git.Repo.git.push')

    runner = CliRunner()
    result = runner.invoke(cli, ['fix'])

    assert result.exit_code == 0
    assert "Fix branch fix/release/v1.0.1 created and pushed." in result.output

def test_fix_branch_creation_failure_not_on_release_branch(mocker):
    mock_repo = mocker.patch('git.Repo')
    mock_branch = Mock()
    mock_branch.name = 'feature/some-feature'
    mock_repo.return_value.active_branch = mock_branch

    runner = CliRunner()
    result = runner.invoke(cli, ['fix'])

    assert result.exit_code != 0
    assert "Fix branches must be created from a release branch." in result.output

def test_major_branch_creation_success(mocker):
    mock_repo = mocker.patch('git.Repo')
    mocker.patch('git.Repo.git.checkout')
    mocker.patch('git.Repo.git.push')

    runner = CliRunner()
    result = runner.invoke(cli, ['major'])

    assert result.exit_code == 0
    assert "Major release branch release/v2.0.0 created and pushed." in result.output

def test_major_branch_creation_failure(mocker):
    mocker.patch('git.Repo', side_effect=GitError("git error"))

    runner = CliRunner()
    result = runner.invoke(cli, ['major'])

    assert result.exit_code != 0
    assert "Error: git error" in result.output

def test_release_branch_creation_without_version(mocker):
    mock_repo = mocker.patch('git.Repo')
    mocker.patch('git.Repo.git.checkout')
    mocker.patch('git.Repo.git.push')

    runner = CliRunner()
    result = runner.invoke(cli, ['release'])

    assert result.exit_code == 0
    assert "Release branch release/v1.0.0 created and pushed." in result.output  # Assuming 1.0.0 is the default version

def test_fix_branch_creation_failure_on_git_error(mocker):
    mock_repo = mocker.patch('git.Repo', side_effect=GitError("git error"))

    runner = CliRunner()
    result = runner.invoke(cli, ['fix'])

    assert result.exit_code != 0
    assert "Error: git error" in result.output