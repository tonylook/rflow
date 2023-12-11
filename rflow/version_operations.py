import json
import semantic_version

def read_current_version():
    """
    Read the current version from the version.info file.
    """
    try:
        with open('version.info', 'r') as file:
            version_info = json.load(file)
        return version_info['currentVersion']
    except (FileNotFoundError, KeyError):
        raise ValueError("version.info file not found or invalid format")

def read_next_version():
    """
    Read the current version from the version.info file.
    """
    try:
        with open('version.info', 'r') as file:
            version_info = json.load(file)
        return version_info['nextVersion']
    except (FileNotFoundError, KeyError):
        raise ValueError("version.info file not found or invalid format")

def increment_major_version(version):
    """
    Increment the major version.
    """
    semver = semantic_version.Version(version)
    return str(semver.next_major())

def increment_minor_version(version):
    """
    Increment the minor version.
    """
    semver = semantic_version.Version(version)
    return str(semver.next_minor())

def increment_patch_version(version):
    """
    Increment the patch version.
    """
    semver = semantic_version.Version(version)
    return str(semver.next_patch())

def get_latest_release_version(repo):
    """
    Get the version number from the latest release branch in the repository.
    """
    release_branches = [branch for branch in repo.branches if branch.name.startswith('release/v')]
    if not release_branches:
        return None

    # Extracting version numbers and sorting them
    versions = []
    for branch in release_branches:
        try:
            version_str = branch.name.split('release/v')[-1]
            versions.append(semantic_version.Version(version_str))
        except ValueError:
            continue  # Ignore branches with invalid version formats

    if not versions:
        return None

    return max(versions)  # Return the highest version
