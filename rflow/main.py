import click
import git
from git.exc import GitError


@click.group()
def cli():
    pass


@cli.command()
@click.option('--version', default='1.0.0', help='Next version number.')
def release(version):
    """
    Create a new release branch.
    """
    try:
        repo = git.Repo('.')
        release_branch = f'release/v{version}'
        repo.git.checkout('HEAD', b=release_branch)
        repo.git.push('origin', release_branch)
        click.echo(f'Release branch {release_branch} created and pushed.')
    except GitError as e:
        click.echo(f'Error: {str(e)}', err=True)


if __name__ == '__main__':
    cli()
