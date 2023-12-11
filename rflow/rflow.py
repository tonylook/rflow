import click
import git
from rflow import utils
from rflow import version_operations
from git.exc import GitError

@click.group()
def cli():
    pass

@cli.command()
@click.option('--version', default=None, help='Specify the version for the release branch.')
def release(version):
    """
    Create a new release branch.
    """
    try:
        repo = git.Repo('.')
        if not version:
            version = "1.0.0"  # Placeholder for current version
        release_branch = f'release/v{version}'
        repo.git.checkout('HEAD', b=release_branch)
        repo.git.push('origin', release_branch)
        click.echo(f'Release branch {release_branch} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()  # This will cause the command to exit with a non-zero status code

@cli.command()
def major():
    """
    Create a new major release branch.
    """
    try:
        repo = git.Repo('.')
        current_version = "1.0.0"  # Placeholder for current version
        major_version = version_operations.increment_major_version(current_version)
        major_release_branch = f'release/v{major_version}'
        repo.git.checkout('HEAD', b=major_release_branch)
        repo.git.push('origin', major_release_branch)
        click.echo(f'Major release branch {major_release_branch} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()  # Ensure non-zero exit on error

@cli.command()
def fix():
    """
    Create a fix branch from the current release branch.
    """
    try:
        repo = git.Repo('.')
        if not utils.is_release_branch(repo.active_branch.name):
            click.echo("Fix branches must be created from a release branch.", err=True)
            raise click.Abort()
        fix_branch = f'fix/{repo.active_branch.name}'
        repo.git.checkout('HEAD', b=fix_branch)
        repo.git.push('origin', fix_branch)
        click.echo(f'Fix branch {fix_branch} created and pushed.')
    except (GitError, Exception) as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()
