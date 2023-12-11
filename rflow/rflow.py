import json
import click
import git
from rflow import git_operations
from rflow import version_operations
from git.exc import GitError

@click.group()
def cli():
    pass

@cli.command()
def release():
    """
    Create a new release branch based on the version from version.info file.
    """
    try:
        repo = git.Repo('.')
        version = version_operations.read_current_version()
        release_branch = f'release/v{version}'
        repo.git.checkout('HEAD', b=release_branch)
        repo.git.push('origin', release_branch)
        click.echo(f'Release branch {release_branch} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()

@cli.command()
def major():
    """
    Create a new major release branch.
    """
    try:
        repo = git.Repo('.')
        current_version = version_operations.read_current_version()
        major_version = version_operations.increment_major_version(current_version)
        major_release_branch = f'release/v{major_version}'
        repo.git.checkout('HEAD', b=major_release_branch)
        repo.git.push('origin', major_release_branch)
        click.echo(f'Major release branch {major_release_branch} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()

@cli.command()
def fix():
    """
    Create a fix branch from the current release branch.
    """
    try:
        repo = git.Repo('.')
        if not git_operations.is_release_branch(repo.active_branch.name):
            click.echo("Fix branches must be created from a release branch.", err=True)
            raise click.Abort()
        fix_branch = f'fix/{repo.active_branch.name}'
        repo.git.checkout('HEAD', b=fix_branch)
        repo.git.push('origin', fix_branch)
        click.echo(f'Fix branch {fix_branch} created and pushed.')
    except (GitError, Exception) as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()

@cli.command()
def init():
    """
    Initialize a version.info file in the current Git repository.
    This command must be run from the 'main' branch.
    """
    try:
        repo = git.Repo('.')

        if repo.active_branch.name != 'main':
            raise ValueError("The 'init' command must be run from the 'main' branch.")

        latest_version = version_operations.get_latest_release_version(repo)
        if latest_version is None:
            raise ValueError("No release branches found in the repository.")

        version_info = {
            "currentVersion": str(latest_version),
            "nextVersion": str(latest_version.next_minor())
        }

        with open('version.info', 'w') as file:
            json.dump(version_info, file, indent=4)

        click.echo("Initialized version.info with version: " + str(latest_version))
    except (GitError, ValueError, Exception) as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()
