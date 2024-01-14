import json
import os
import datetime
import click
from rflow import git_operations
from rflow import version_operations
from git.exc import GitError


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    :param ctx: the click Context object
    :return: None

    This method is a click command group with the `invoke_without_command=True` option. It allows the CLI to be invoked without any subcommand. If no subcommand is provided, it will display
    * a message using `click.echo()`.

    Example usage:
        cli()
    """
    if ctx.invoked_subcommand is None:
        click.echo("rflow: try 'rflow --help' for more information")


@cli.command()
def release():
    """
    Release Method

    This method is used to create and push a release branch on a Git repository.

    :return: None
    """
    try:
        repo = git_operations.initialize_repo()
        main_branch_name = git_operations.get_main_branch_name(repo)
        git_operations.check_active_branch(repo, main_branch_name)
        version = version_operations.read_next_version()
        release_branch = f'release/v{version}'
        repo.git.checkout(main_branch_name, b=release_branch)
        repo.git.push('--set-upstream', 'origin', release_branch)
        click.echo(f'Release branch {release_branch} created and pushed.')
    except GitError as e:
        git_operations.handle_git_error(e)


@cli.command()
def major():
    """
    Create and push a major release branch.

    :return: None
    """
    try:
        repo = git_operations.initialize_repo()
        main_branch_name = git_operations.get_main_branch_name(repo)
        git_operations.check_active_branch(repo, main_branch_name)
        current_version = version_operations.read_current_version()
        major_version = version_operations.increment_major_version(current_version)
        major_release_branch = f'release/v{major_version}'
        repo.git.checkout(main_branch_name, b=major_release_branch)
        repo.git.push('--set-upstream', 'origin', major_release_branch)
        click.echo(f'Major release branch {major_release_branch} created and pushed.')
    except GitError as e:
        git_operations.handle_git_error(e)


@cli.command()
@click.argument('tag_version', type=str)
@click.argument('bug_description', type=str)
def fix(tag_version, bug_description):
    """
    :param tag_version: The version number of the tag to fix the bug from.
    :param bug_description: A description of the bug that is being fixed.
    :return: None

    This method is a command line interface command that creates a new fix branch and pushes it to the remote repository. The fix branch is created from a release branch corresponding to
    * the provided tag version.

    Example usage:
    fix("1.0.3", "bug-fix")
    """
    try:
        repo = git_operations.initialize_repo()
        tag = f'v{tag_version}'
        if tag not in repo.tags:
            click.echo(f"Tag {tag} not found.", err=True)
            raise click.Abort()
        release_branch_name = f"release/v{tag_version.rsplit('.', 1)[0]}.0"
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
        git_operations.handle_git_error(e)


@cli.command()
def init():
    """
    Initializes the repository and creates a version.info file with the current and next versions.

    :return: None
    """
    try:
        repo = git_operations.initialize_repo()
        main_branch_name = git_operations.get_main_branch_name(repo)
        git_operations.check_active_branch(repo, main_branch_name)
        if os.path.exists('version.info'):
            click.echo("version.info file already exists. Initialization aborted.")
            return
        latest_version = version_operations.get_latest_release_version(repo)
        if latest_version:
            current_version = latest_version
            next_version = version_operations.increment_minor_version(latest_version)
        else:
            current_version = version_operations.init_version()
            next_version = current_version
        version_info = {
            "currentVersion": current_version,
            "nextVersion": next_version
        }
        with open('version.info', 'w') as file:
            json.dump(version_info, file, indent=4)
        click.echo(f"Initialized version.info with version: {version_info['currentVersion']}")
    except (GitError, Exception) as e:
        git_operations.handle_git_error(e)


@cli.command()
def version():
    """
    Get the current version from the 'version.info' file.

    :return: None
    """
    try:
        if not os.path.exists('version.info'):
            click.echo("version.info file does not exist. Please initialize it using 'rflow init'.")
            raise click.Abort()
        with open('version.info', 'r') as file:
            version_info = json.load(file)
            current_version = version_info.get("currentVersion", "Unknown")
        click.echo(f"Current version: {current_version}")
    except Exception as e:
        click.echo(f'Error: {str(e)}', err=True)
        raise click.Abort()


@cli.command()
def snap():
    """
    Create a snapshot tag and push it to the remote repository.

    :return: None
    """
    try:
        repo = git_operations.initialize_repo()
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
@click.option('-f', '--force', is_flag=True, help='Force tag creation, overwriting if it already exists.')
def tag(force):
    """
    :param force: (boolean) Whether to force tag creation, overwriting if it already exists.
    :return: None

    This method is a command-line interface command for creating and pushing tags in a Git repository. The optional `--force` flag can be used to force tag creation, overwriting the tag
    * if it already exists. The method performs the following steps:

    1. Initializes the Git repository.
    2. Checks if the current branch is a release branch.
    3. Reads the current version from the project.
    4. Constructs the tag name using the current version.
    5. Checks if the tag already exists in the repository.
       - If the `--force` flag is used, the existing tag is deleted and a new tag is created with the same name.
       - If the `--force` flag is not used, a message is displayed and the method returns without creating the tag.
    6. Creates the new tag and pushes it to the remote repository.

    If any error occurs during the execution of the method, it is caught and handled by the `handle_git_error` function.
    """
    try:
        repo = git_operations.initialize_repo()
        branch_name = repo.active_branch.name
        if not git_operations.is_release_branch(branch_name):
            click.echo("Tag command must be run from a release branch.")
            raise click.Abort()
        version = version_operations.read_current_version()
        tag_name = f'v{version}'
        if tag_name in repo.tags:
            if force:
                click.echo(f"Tag {tag_name} already exists. Overwriting due to --force option.")
                repo.delete_tag(tag_name)
                repo.create_tag(tag_name)
                repo.git.push('origin', '--delete', tag_name)
                repo.git.push('origin', tag_name)
            else:
                click.echo(f"Tag {tag_name} already exists. Use --force to overwrite.")
                return
        else:
            repo.create_tag(tag_name)
            repo.git.push('origin', tag_name)
        click.echo(f'Tag {tag_name} {"overwritten" if force else "created"} and pushed.')
    except GitError as e:
        git_operations.handle_git_error(e)


if __name__ == '__main__':
    cli()
