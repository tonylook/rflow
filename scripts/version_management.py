import json
import subprocess
import sys


def run_git_command(command):
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Git command: {e.output.decode()}")
        sys.exit(1)


def update_version_info(file_path, current_version, next_version):
    with open(file_path, 'r+') as file:
        version_info = json.load(file)
        version_info['currentVersion'] = current_version
        version_info['nextVersion'] = next_version
        file.seek(0)
        json.dump(version_info, file, indent=4)
        file.truncate()


def increment_version(version, increment_minor=True):
    major, minor, patch = map(int, version.split('.'))
    if increment_minor:
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def get_default_branch():
    """Determine the default branch name (main or master)."""
    branches = subprocess.check_output("git branch -r", shell=True).decode().split()
    if 'origin/main' in branches:
        return 'main'
    elif 'origin/master' in branches:
        return 'master'
    else:
        raise ValueError("Default branch (main/master) not found.")


def handle_release_branch(release_branch):
    default_branch = get_default_branch()

    # Check out default branch (main or master) and update version.info
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

    # Check out release branch and update version.info
    run_git_command(f"git checkout -b {release_branch}")
    next_patch_version = increment_version(current_version, increment_minor=False)
    update_version_info('version.info', current_version, next_patch_version)
    run_git_command("git add version.info")
    run_git_command("git commit -m 'Prepare release branch with version info'")
    run_git_command(f"git push origin {release_branch}")


def handle_fix_branch(release_branch, fix_branch):
    # Check out the release branch and update version.info
    run_git_command(f"git checkout {release_branch}")
    run_git_command(f"git pull origin {release_branch}")
    with open('version.info', 'r+') as file:
        version_info = json.load(file)
        next_version = increment_version(version_info['nextVersion'], increment_minor=False)

    # Update version.info in release branch
    update_version_info('version.info', version_info['currentVersion'], next_version)
    run_git_command("git add version.info")
    run_git_command("git commit -m 'Increment patch version in release branch'")
    run_git_command(f"git push origin {release_branch}")

    # Update version.info in fix branch
    run_git_command(f"git checkout -b {fix_branch} {release_branch}")
    run_git_command("git add version.info")
    run_git_command(f"git commit -m 'Sync version info with release branch'")
    run_git_command(f"git push --set-upstream origin {fix_branch}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python version_management.py <command> [options]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "release" and len(sys.argv) == 3:
        release_branch = sys.argv[2]
        handle_release_branch(release_branch)
    elif command == "fix" and len(sys.argv) == 4:
        release_branch = sys.argv[2]
        fix_branch = sys.argv[3]
        handle_fix_branch(release_branch, fix_branch)
    else:
        print("Invalid usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
