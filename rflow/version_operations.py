import json
import os
import click
import semantic_version


def update_version_info(file_path, current_version, next_version):
    """
    Update the version information in a JSON file.
    :param file_path: The path to the JSON file to be updated.
    :type file_path: str
    :param current_version: The current version.
    :type current_version: str
    :param next_version: The next version.
    :type next_version: str
    """
    with open(file_path, 'r+') as file:
        version_info = json.load(file)
        version_info['currentVersion'] = current_version
        version_info['nextVersion'] = next_version
        file.seek(0)
        json.dump(version_info, file, indent=4)
        file.truncate()


def read_current_version():
    """
    Read the current version from the 'version.info' file.
    :return: The current version as a string.
    :raises ValueError: If the 'version.info' file is not found or has an invalid format.
    """
    try:
        check_version_info_exists()
        with open('version.info', 'r') as file:
            version_info = json.load(file)
        return version_info['currentVersion']
    except (FileNotFoundError, KeyError):
        raise ValueError("version.info file not found or invalid format")


def read_next_version():
    """
    Read the next version from a version.info file.
    :return: The next version as specified in the version.info file.
    :raises ValueError: If the version.info file is not found or has an invalid format.
    """
    try:
        check_version_info_exists()
        with open('version.info', 'r') as file:
            version_info = json.load(file)
        return version_info['nextVersion']
    except (FileNotFoundError, KeyError):
        raise ValueError("version.info file not found or invalid format")


def increment_major_version(version):
    """
    :param version: The current version in semantic versioning format (e.g. "1.2.3").
    :return: The incremented version with the major version number increased by 1 (e.g. "2.0.0").
    """
    semver = semantic_version.Version(version)
    return str(semver.next_major())


def increment_minor_version(version):
    """
    Increments the minor version of a given version.
    :param version: A string representing the current version in semantic versioning format (MAJOR.MINOR.PATCH)
    :return: A string representing the next minor version in semantic versioning format (MAJOR.MINOR.PATCH)
    """
    semver = semantic_version.Version(version)
    return str(semver.next_minor())


def increment_patch_version(version):
    """
    :param version: The current version in semantic versioning format (e.g. "1.2.3").
    :return: The incremented version with the patch number increased by 1 (e.g. "1.2.4").
    """
    semver = semantic_version.Version(version)
    return str(semver.next_patch())


def get_latest_release_version(repo):
    """
    Get the latest release version from a given repository.
    :param repo: The repository to get the latest release version from.
    :return: The latest release version as a string, or None if no release branches are found or there are no versions available.
    """
    release_branches = [branch for branch in repo.branches if branch.name.startswith('release/v')]
    if not release_branches:
        return None
    versions = []
    for branch in release_branches:
        try:
            version_str = branch.name.split('release/v')[-1]
            versions.append(semantic_version.Version(version_str))
        except ValueError:
            continue  # Ignore branches with invalid version formats
    if not versions:
        return None
    return str(max(versions))  # Return the highest version


def check_version_info_exists():
    """
    Function to check if a 'version.info' exists in the current directory.
    Raises a FileNotFoundError if 'version.info' does not exist.
    :return: None
    """
    if not os.path.exists('version.info'):
        click.echo("version.info file does not exist. Please initialize it using 'rflow init'.")
        raise click.Abort()


def init_version():
    """
    This method initializes a version number and returns it as a string.
    :return: The initialized version as a string.
    """
    semver = semantic_version.Version('1.0.0')
    return str(semver)
