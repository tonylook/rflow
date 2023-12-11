import git
def create_branch(branch_name):
    repo = git.Repo('.')
    repo.git.checkout('HEAD', b=branch_name)

def push_branch(branch_name):
    repo = git.Repo('.')
    repo.git.push('origin', branch_name)

def is_release_branch(branch_name):
    return branch_name.startswith('release/v')