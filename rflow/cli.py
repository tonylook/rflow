import json
import os
import datetime
import click
import git
from rflow import git_operations
from rflow import version_operations
from git.exc import GitError


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """rflow CLI tool for release flow management."""
    if ctx.invoked_subcommand is None:
        click.echo("rflow: try 'rflow --help' for more information")


@cli.command()
def release():
    """Create a new release branch from the main or master branch."""
    try:
        repo = git.Repo('.')
        main_branch_name = git_operations.get_main_branch_name(repo)
        if repo.active_branch.name != main_branch_name:
            click.echo(f"Release command must be run from the {main_branch_name} branch.")
            raise click.Abort()

        version = version_operations.read_next_version()
        release_branch = f'release/v{version}'
        repo.git.checkout(main_branch_name, b=release_branch)
        repo.git.push('--set-upstream', 'origin', release_branch)
        click.echo(f'Release branch {release_branch} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


@cli.command()
def major():
    """Create a new major release branch from the main or master branch."""
    try:
        repo = git.Repo('.')
        main_branch_name = git_operations.get_main_branch_name(repo)
        if repo.active_branch.name != main_branch_name:
            click.echo(f"Major command must be run from the {main_branch_name} branch.")
            raise click.Abort()

        current_version = version_operations.read_current_version()
        major_version = version_operations.increment_major_version(current_version)
        major_release_branch = f'release/v{major_version}'
        repo.git.checkout(main_branch_name, b=major_release_branch)
        repo.git.push('--set-upstream', 'origin', major_release_branch)
        click.echo(f'Major release branch {major_release_branch} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


@cli.command()
@click.argument('tag_version', type=str)
@click.argument('bug_description', type=str)
def fix(tag_version, bug_description):
    """Create a fix branch from a specified tag version."""
    try:
        repo = git.Repo('.')
        tag = f'v{tag_version}'
        if tag not in repo.tags:
            click.echo(f"Tag {tag} not found.", err=True)
            raise click.Abort()

        release_branch_name = f'release/v{tag_version}'
        if release_branch_name in repo.branches:
            repo.git.checkout(release_branch_name)
        else:
            click.echo(f"Tag {tag} is not on a release branch. Please proceed manually.")
            return

        fix_branch_name = f'fix/{bug_description}-from-{tag_version}'
        repo.git.checkout('HEAD', b=fix_branch_name)
        repo.git.push('--set-upstream', 'origin', fix_branch_name)
        click.echo(f'Fix branch {fix_branch_name} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


@cli.command()
def init():
    """
    Initialize a version.info file in the current Git repository.
    Only works on 'main' or 'master' branch.
    """
    try:
        repo = git.Repo('.')
        main_branch_name = git_operations.get_main_branch_name(repo)
        if repo.active_branch.name != main_branch_name:
            click.echo(f"The 'init' command must be run from the '{main_branch_name}' branch.")
            raise click.Abort()

        if os.path.exists('version.info'):
            click.echo("version.info file already exists. Initialization aborted.")
            return

        latest_version = version_operations.get_latest_release_version(repo)

        version_info = {
            "currentVersion": latest_version or "1.0.0",
            "nextVersion": version_operations.increment_minor_version(latest_version or "1.0.0")
        }

        with open('version.info', 'w') as file:
            json.dump(version_info, file, indent=4)

        click.echo(f"Initialized version.info with version: {version_info['currentVersion']}")
    except (GitError, Exception) as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


@cli.command()
def snap():
    """Create a snapshot tag for the current branch."""
    try:
        repo = git.Repo('.')
        version = version_operations.read_current_version()
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        snapshot_tag = f'v{version}-{timestamp}'
        repo.create_tag(snapshot_tag)
        repo.git.push('origin', snapshot_tag)
        click.echo(f'Snapshot tag {snapshot_tag} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


@cli.command()
def tag():
    """
    Create a Git tag from the current version on release branches.
    """
    try:
        repo = git.Repo('.')
        branch_name = repo.active_branch.name

        if not git_operations.is_release_branch(branch_name):
            click.echo("Tag command must be run from a release branch.")
            raise click.Abort()

        version = version_operations.read_current_version()
        tag_name = f'v{version}'

        # Check if the tag already exists
        if tag_name in repo.tags:
            click.echo(f"Tag {tag_name} already exists.")
            return

        repo.create_tag(tag_name)
        repo.git.push('origin', tag_name)
        click.echo(f'Tag {tag_name} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


if __name__ == '__main__':
    cli()
