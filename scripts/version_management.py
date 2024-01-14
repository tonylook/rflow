import json
import subprocess
import sys


def run_git_command(command):
    """
    Runs a Git command and returns the output.

    :param command: the Git command to execute
    :return: the output of the Git command
    """
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error for the Git command: {command} --> output: {e.output}")
        sys.exit(1)


def update_version_info(file_path, current_version, next_version):
    """
    Update the version information in a JSON file.

    :param file_path: The path to the JSON file to be updated.
    :type file_path: str
    :param current_version: The current version.
    :type current_version: str
    :param next_version: The next version.
    :type next_version: str
    :return: None
    :rtype: None
    """
    with open(file_path, 'r+') as file:
        version_info = json.load(file)
        version_info['currentVersion'] = current_version
        version_info['nextVersion'] = next_version
        file.seek(0)
        json.dump(version_info, file, indent=4)
        file.truncate()


def increment_version(version, increment_minor=True):
    """
    Increment the given version number.

    :param version: The version number in format 'major.minor.patch'.
    :param increment_minor: Flag to specify whether to increment the minor version or the patch version.
                            Defaults to True, which increments the minor version.
    :return: The incremented version number.
    """
    major, minor, patch = map(int, version.split('.'))
    if increment_minor:
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def get_default_branch():
    """
    Returns the default branch of a Git repository.

    :return: The default branch name (either 'main' or 'master').
    :rtype: str
    :raises ValueError: If the default branch (main/master) is not found.
    """
    branches = subprocess.check_output("git branch -r", shell=True).decode().split()
    if 'origin/main' in branches:
        return 'main'
    elif 'origin/master' in branches:
        return 'master'
    else:
        raise ValueError("Default branch (main/master) not found.")


def handle_release_branch(release_branch):
    """
    :param release_branch: The name of the release branch to handle.
    :return: None

    This method handles the release branch by performing a series of Git commands and updating the version info.

    If the specified release branch is not at its first commit or not the latest version, a message will be printed and the method will return without making any changes.

    Otherwise, the method will proceed with the following steps:
    1. Get the default branch.
    2. Checkout and pull the latest changes from the default branch.
    3. Load the version info from the 'version.info' file.
    4. Get the current version and increment it to get the next version.
    5. Update the version info with the new current and next versions.
    6. Add and commit the updated version info to the default branch.
    7. Push the changes to the remote repository.
    8. Checkout the release branch.
    9. Increment the current version to the next patch version.
    10. Update the version info with the new current and next versions.
    11. Add and commit the updated version info to the release branch.
    12. Push the changes to the remote repository.
    """
    if not is_first_commit_in_branch(release_branch):
        print(f"{release_branch} is not at its first commit or not the latest version.")
        return
    default_branch = get_default_branch()
    run_git_command(f"git checkout {default_branch}")
    run_git_command(f"git pull origin {default_branch}")
    with open('version.info', 'r+') as file:
        version_info = json.load(file)
        current_version = version_info['nextVersion']
        next_version = increment_version(current_version)
    update_version_info('version.info', current_version, next_version)
    run_git_command("git add version.info")
    run_git_command("git commit -m 'Update version.info for new release'")
    run_git_command(f"git push origin {default_branch}")
    run_git_command(f"git checkout {release_branch}")
    next_patch_version = increment_version(current_version, increment_minor=False)
    update_version_info('version.info', current_version, next_patch_version)
    run_git_command("git add version.info")
    run_git_command("git commit -m 'Prepare release branch with version info'")
    run_git_command(f"git push origin {release_branch}")


def handle_fix_branch(fix_branch):
    """
    :param fix_branch: The name of the fix branch to handle.
    :return: None

    This method handles the creation and updating of a fix branch in a git repository. It performs the following steps:
    1. Extracts the current version from the version.info file.
    2. Increments the next version based on the current version.
    3. Modifies the version for the release branch by setting the patch level to 0.
    4. Checks out and updates the release branch.
    5. Updates the version info in the version.info file for the release branch.
    6. Commits the changes to the version.info file on the release branch.
    7. Pushes the changes to the remote repository for the release branch.
    8. Checks out and updates the fix branch.
    9. Updates the version info in the version.info file for the fix branch.
    10. Commits the changes to the version.info file on the fix branch.
    11. Pushes the changes to the remote repository for the fix branch.
    """
    # Extract current version from version.info
    with open('version.info', 'r') as file:
        version_info = json.load(file)
        current_version = version_info['nextVersion']
        next_version = increment_version(current_version, increment_minor=False)
    branch_version = f"{current_version.rsplit('.', 1)[0]}.0"
    # Checkout and update the release branch
    run_git_command(f"git checkout release/v{branch_version}")
    run_git_command(f"git pull origin release/v{branch_version}")
    update_version_info('version.info', current_version, next_version)
    run_git_command("git add version.info")
    run_git_command("git commit -m 'Update version.info for release branch'")
    run_git_command(f"git push origin release/v{branch_version}")
    # Checkout and update the fix branch
    run_git_command(f"git checkout {fix_branch}")
    run_git_command(f"git pull origin {fix_branch}")
    update_version_info('version.info', current_version, next_version)
    run_git_command("git add version.info")
    run_git_command("git commit -m 'Prepare fix branch with version info'")
    run_git_command(f"git push origin {fix_branch}")


def extract_branch_name(source_branch):
    """
    Extracts the branch name from the given source_branch.

    :param source_branch: The source branch name.
    :type source_branch: str
    :return: The extracted branch name.
    :rtype: str
    :raises ValueError: If the given source_branch is not supported.
    """
    if 'release/' in source_branch:
        return source_branch.partition('release/')[1] + source_branch.partition('release/')[2]
    elif 'fix/' in source_branch:
        return source_branch.partition('fix/')[1] + source_branch.partition('fix/')[2]
    else:
        raise ValueError(f"Branch name not supported: {source_branch}")


def is_first_commit_in_branch(branch_name):
    """
    :param branch_name: The name of the branch to check if it is the first commit.
    :return: True if the branch is the first commit, False otherwise.

    """
    try:
        run_git_command("git fetch")
        full_branch_name = f"origin/{branch_name}"
        first_commit_in_branch = run_git_command(f"git rev-list --max-parents=0 {full_branch_name}")
        last_commit_in_repo = run_git_command("git rev-parse HEAD")
        return first_commit_in_branch == last_commit_in_repo
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def is_first_commit_in_fix_branch(fix_branch):
    """
    :param fix_branch: The name of the fix branch to check
    :return: True if the fix branch has no commits ahead of the release branch, False otherwise
    """
    try:
        run_git_command("git fetch")
        run_git_command(f"git checkout {fix_branch}")
        with open('version.info', 'r') as file:
            version_info = json.load(file)
            current_version = version_info['currentVersion']
        release_branch = f"origin/release/v{current_version.rsplit('.', 1)[0]}.0"
        full_fix_branch = f"origin/{fix_branch}"
        commits_diff = run_git_command(f"git rev-list --count {release_branch}..{full_fix_branch}")
        return commits_diff == "0"
    except Exception as e:
        print(f"Error in is_first_commit_in_fix_branch: {e}")
        raise


def main():
    """
    Entry point for the version management script.

    :return: None
    """
    if len(sys.argv) < 3:
        print("Usage: python version_management.py <command> <ref>")
        sys.exit(1)
    command = sys.argv[1]
    ref = sys.argv[2]
    branch = extract_branch_name(ref)
    if command == "release":
        if not is_first_commit_in_branch(branch):
            print(f"Not the first commit in {branch}. Exiting script.")
            return
        handle_release_branch(branch)
    elif command == "fix":
        if not is_first_commit_in_fix_branch(branch):
            print(f"Not the first commit in {branch} or already diverged from release branch. Exiting script.")
            return
        handle_fix_branch(branch)
    else:
        print("Invalid usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
