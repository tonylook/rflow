import json
import subprocess
import sys


def run_git_command(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
        return output.strip()
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
    run_git_command(f"git checkout {release_branch}")
    next_patch_version = increment_version(current_version, increment_minor=False)
    update_version_info('version.info', current_version, next_patch_version)
    run_git_command("git add version.info")
    run_git_command("git commit -m 'Prepare release branch with version info'")
    run_git_command(f"git push origin {release_branch}")

def extract_branch_name(source_branch):
    if 'release/' in source_branch:
        return source_branch.partition('release/')[1] + source_branch.partition('release/')[2]
    elif 'fix/' in source_branch:
        return source_branch.partition('fix/')[1] + source_branch.partition('fix/')[2]
    else:
        raise ValueError(f"Branch name not supported: {source_branch}")

def is_first_commit_in_branch(branch_name):
    try:
        run_git_command("git fetch")
        full_branch_name = f"origin/{branch_name}"

        first_commit_in_branch = run_git_command(f"git rev-list --max-parents=0 {full_branch_name}")
        last_commit_in_repo = run_git_command("git rev-parse HEAD")

        is_first = first_commit_in_branch == last_commit_in_repo
        print(f"Is first commit in {branch_name}: {is_first}")

        return is_first

    except Exception as e:
        print(f"Errore: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python version_management.py <command> <branch>")
        sys.exit(1)

    command = sys.argv[1]
    branch = extract_branch_name(sys.argv[2])

    if not is_first_commit_in_branch(branch):
        print(f"Not the first commit in {branch}. Exiting script.")
        return
    if command == "release":
        handle_release_branch(branch)
    elif command == "fix":
        handle_fix_branch(branch)
    else:
        print("Invalid usage.")
        sys.exit(1)

if __name__ == "__main__":
    main()

