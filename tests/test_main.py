from unittest.mock import Mock

from click.testing import CliRunner
from git.exc import GitError

from rflow.rflow import cli
import semantic_version


def test_release_branch_creation_failure(mocker):
    mocker.patch('git.Repo', side_effect=GitError("git error"))
    mocker.patch('rflow.version_operations.read_current_version', return_value='1.0.1')

    runner = CliRunner()
    result = runner.invoke(cli, ['release'])

    assert result.exit_code != 0
    assert "Error: git error" in result.output

def test_release_branch_creation_success(mocker):
    expected_version = '1.0.1'
    mock_repo = mocker.patch('git.Repo')
    mocker.patch('git.Repo.git.checkout')
    mocker.patch('git.Repo.git.push')
    mocker.patch('rflow.version_operations.read_current_version', return_value=expected_version)

    runner = CliRunner()
    result = runner.invoke(cli, ['release'])

    assert result.exit_code == 0
    assert f"Release branch release/v{expected_version} created and pushed." in result.output


def test_fix_branch_creation_success(mocker):
    current_branch_name = 'release/v1.0.1'
    expected_fix_branch = f'fix/{current_branch_name}'
    mock_repo = mocker.patch('git.Repo')
    mock_branch = Mock()
    mock_branch.name = current_branch_name
    mock_repo.return_value.active_branch = mock_branch
    mocker.patch('git.Repo.git.checkout')
    mocker.patch('git.Repo.git.push')

    runner = CliRunner()
    result = runner.invoke(cli, ['fix'])

    assert result.exit_code == 0
    assert f"Fix branch {expected_fix_branch} created and pushed." in result.output




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
    mocker.patch('rflow.version_operations.read_current_version', return_value='1.0.0')
    mocker.patch('rflow.version_operations.increment_major_version', return_value='2.0.0')

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


def test_fix_branch_creation_failure_on_git_error(mocker):
    mock_repo = mocker.patch('git.Repo', side_effect=GitError("git error"))

    runner = CliRunner()
    result = runner.invoke(cli, ['fix'])

    assert result.exit_code != 0
    assert "Error: git error" in result.output


def test_init_success(mocker):
    mock_repo = mocker.patch('git.Repo')
    mock_branch = Mock()
    mock_branch.name = 'main'
    mock_repo.return_value.active_branch = mock_branch

    mocker.patch('rflow.version_operations.get_latest_release_version', return_value=semantic_version.Version('1.0.0'))
    mocker.patch('builtins.open', mocker.mock_open())

    runner = CliRunner()
    result = runner.invoke(cli, ['init'])

    assert result.exit_code == 0
    assert "Initialized version.info with version: 1.0.0" in result.output


def test_init_failure_not_on_main(mocker):
    mock_repo = mocker.patch('git.Repo')
    mock_branch = Mock()
    mock_branch.name = 'feature-branch'
    mock_repo.return_value.active_branch = mock_branch

    runner = CliRunner()
    result = runner.invoke(cli, ['init'])

    assert result.exit_code != 0
    assert "The 'init' command must be run from the 'main' branch." in result.output


def test_init_failure_no_release_branches(mocker):
    mock_repo = mocker.patch('git.Repo')
    mock_branch = Mock()
    mock_branch.name = 'main'
    mock_repo.return_value.active_branch = mock_branch

    mocker.patch('rflow.version_operations.get_latest_release_version', return_value=None)

    runner = CliRunner()
    result = runner.invoke(cli, ['init'])

    assert result.exit_code != 0
    assert "No release branches found in the repository." in result.output
