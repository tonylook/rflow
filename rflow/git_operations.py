import click
import git
from git import GitError


def is_release_branch(branch_name):
    """
    Determines if a branch is a release branch.

    :param branch_name: The name of the branch.
    :return: True if the branch is a release branch, False otherwise.
    """
    return branch_name.startswith('release/v')

def get_main_branch_name(repo):
    """
    Get the name of the main branch in the given repository.

    :param repo: The repository object.
    :type repo: Repository
    :return: The name of the main branch.
    :rtype: str
    :raises ValueError: If 'main' or 'master' branch is not found in the repository.
    """
    if 'main' in repo.branches:
        return 'main'
    elif 'master' in repo.branches:
        return 'master'
    else:
        raise ValueError("'main' or 'master' not found in repository.")
def initialize_repo():
    """
    Initializes a git repository in the current directory.

    :return: A `git.Repo` object representing the initialized repository.
    """
    try:
        return git.Repo('.')
    except GitError as e:
        handle_git_error(e)

def check_active_branch(repo, main_branch_name):
    """
    Checks if the active branch in the given repository matches the provided main branch name.

    :param repo: The repository to check.
    :param main_branch_name: The name of the main branch.
    :return: None.
    :raises click.Abort: If the active branch does not match the main branch name.
    """
    if repo.active_branch.name != main_branch_name:
        click.echo(f"Command must be run from the {main_branch_name} branch.")
        raise click.Abort()

def handle_git_error(e):
    """
    :param e: The exception object raised by the Git operation.
    :return: None
    """
    click.echo(f'Error: {str(e)}', err=True)
    raise click.Abort()