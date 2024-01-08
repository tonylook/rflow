import json
import os

import click
import git
from rflow import git_operations
from rflow import version_operations
from git.exc import GitError


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("rflow: try 'rflow --help' for more information")
    pass


@cli.command()
def release():
    """
    Create a new release branch based on the version from version.info file.
    """
    try:
        repo = git.Repo('.')
        version = version_operations.read_next_version()
        release_branch = f'release/v{version}'
        repo.git.checkout('HEAD', b=release_branch)
        repo.git.push('--set-upstream', 'origin', release_branch)
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
        repo.git.push('--set-upstream', 'origin', major_release_branch)
        click.echo(f'Major release branch {major_release_branch} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


@cli.command()
@click.argument('pbi_description', type=str)
def fix(pbi_description):
    """
    Create a fix branch from the current release branch with a specified PBI description.
    """
    try:
        repo = git.Repo('.')
        if not git_operations.is_release_branch(repo.active_branch.name):
            click.echo("Fix branches must be created from a release branch.", err=True)
            raise click.Abort()

        fix_branch = f'fix/{pbi_description}'
        repo.git.checkout('HEAD', b=fix_branch)
        repo.git.push('--set-upstream', 'origin', fix_branch)
        click.echo(f'Fix branch {fix_branch} created and pushed.')
    except (GitError, Exception) as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


@cli.command()
def init():
    """
    Initialize a version.info file in the current Git repository.
    This command must be run from the 'main/master' branch.
    """
    try:
        # Check if version.info already exists
        if os.path.exists('version.info'):
            click.echo("version.info file already exists. Initialization aborted.")
            return  # Exit the function early

        repo = git.Repo('.')

        if repo.active_branch.name not in ['main', 'master']:
            click.echo("The 'init' command must be run from the 'main' or 'master' branch.")
            raise click.Abort()

        latest_version = version_operations.get_latest_release_version(repo)

        # Default to version 1.0.0 if no release branches are found
        if latest_version is None:
            latest_version = version_operations.init_version()
            next_version = latest_version
        else:
            next_version = version_operations.increment_minor_version(latest_version)
        version_info = {
            "currentVersion": latest_version,
            "nextVersion": next_version
        }

        with open('version.info', 'w') as file:
            json.dump(version_info, file, indent=4)

        click.echo("Initialized version.info with version: " + str(latest_version))
    except (GitError, Exception) as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


@cli.command()
def tag():
    """
    Create a Git tag from the current version in the version.info file.
    """
    try:
        repo = git.Repo('.')
        current_version = version_operations.read_current_version()

        tag_name = f'v{current_version}'
        repo.create_tag(tag_name)
        repo.git.push('origin', tag_name)

        click.echo(f'Tag {tag_name} created and pushed.')
    except (GitError, Exception) as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()
