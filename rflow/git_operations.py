import git
def create_branch(branch_name):
    repo = git.Repo('.')
    repo.git.checkout('HEAD', b=branch_name)

def push_branch(branch_name):
    repo = git.Repo('.')
    repo.git.push('origin', branch_name)