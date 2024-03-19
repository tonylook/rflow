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
    This method is a click command group with the `invoke_without_command=True` option. It allows the CLI to be invoked
    without any subcommand. If no subcommand is provided, it will display a message using `click.echo()`.
    Example usage:
        cli()
    """
    if ctx.invoked_subcommand is None:
        click.echo("rflow: try 'rflow --help' for more information")
    git_operations.check_if_git_repo()


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
        target_version = version_operations.read_next_version()
        # Update version.info on main branch
        current_version = target_version
        next_version = version_operations.increment_minor_version(target_version)
        version_operations.update_version_info('version.info', current_version, next_version)
        repo.git.add('version.info')
        repo.git.commit('-m', 'Update version.info on main branch')
        # Push changes to main branch
        repo.git.push('--set-upstream', 'origin', main_branch_name)
        # Create and switch to release branch
        release_branch = f'release/v{target_version}'
        repo.git.checkout(main_branch_name, b=release_branch)
        # Update version.info on release branch
        next_version = version_operations.increment_patch_version(target_version)
        version_operations.update_version_info('version.info', current_version, next_version)
        repo.git.add('version.info')
        repo.git.commit('-m', 'Update version.info on release branch')
        # Push release branch
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
        # Update version.info on main branch
        next_minor_version = version_operations.increment_minor_version(major_version)
        version_operations.update_version_info('version.info', major_version, next_minor_version)
        repo.git.add('version.info')
        repo.git.commit('-m', 'Update version.info on main branch')
        # Push changes to main branch
        repo.git.push('--set-upstream', 'origin', main_branch_name)
        # Create and switch to major release branch
        major_release_branch = f'release/v{major_version}'
        repo.git.checkout(main_branch_name, b=major_release_branch)
        # Update version.info on major release branch
        next_patch_version = version_operations.increment_patch_version(major_version)
        version_operations.update_version_info('version.info', major_version, next_patch_version)
        repo.git.add('version.info')
        repo.git.commit('-m', 'Update version.info on major release branch')
        # Push major release branch
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
    This method creates a new fix branch and pushes it to the remote repository.
    The fix branch is created from a release branch corresponding to the provided tag version.
    Example usage:
    rflow fix 1.0.3 bug-fix
    """
    try:
        repo = git_operations.initialize_repo()
        tag = f'v{tag_version}'
        if tag not in repo.tags:
            click.echo(f"Tag {tag} not found.", err=True)
            raise click.Abort()
        repo.git.checkout(tag)
        current_version = version_operations.read_next_version()
        release_branch_name = f"release/v{current_version[:-2]}.0"
        if release_branch_name not in repo.branches:
            click.echo(f"Release branch {release_branch_name} does not exist for tag {tag}. Creating it.")
            repo.git.checkout('-b', release_branch_name)
        repo.git.checkout(release_branch_name)
        next_patch_version = version_operations.increment_patch_version(current_version)
        version_operations.update_version_info('version.info', current_version, next_patch_version)
        repo.git.add('version.info')
        repo.git.commit('-m', 'Update version.info on release branch')
        repo.git.push('--set-upstream', 'origin', release_branch_name)
        click.echo(f'Release branch {release_branch_name} updated and pushed.')
        fix_branch_name = f'fix/{bug_description}-from-{tag_version}'
        repo.git.checkout(tag, b=fix_branch_name)
        version_operations.update_version_info('version.info', current_version, next_patch_version)
        repo.git.add('version.info')
        repo.git.commit('-m', 'Update version.info on fix branch')
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
        # Update version.info file
        version_operations.update_version_info('version.info', current_version, next_version)
        click.echo(f"Initialized version.info with version: {current_version}")
    except (GitError, Exception) as e:
        git_operations.handle_git_error(e)


@cli.command()
def version():
    """
    Get the current version from the 'version.info' file.
    :return: None
    """
    try:
        current_version = version_operations.read_current_version()
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
        active_branch = repo.active_branch.name
        main_branch_name = git_operations.get_main_branch_name(repo)
        if active_branch == main_branch_name:
            version = version_operations.read_next_version()
        else:
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
    This method is for creating and pushing tags. The optional `--force` flag can be used to overwrite the tag.
    """
    try:
        repo = git_operations.initialize_repo()
        branch_name = repo.active_branch.name
        if not git_operations.is_release_branch(branch_name):
            click.echo("Tag command must be run from a release branch.")
            raise click.Abort()
        target_version = version_operations.read_current_version()
        tag_name = f'v{target_version}'
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
