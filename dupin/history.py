import os

from git import Repo


def history(root, message, notification_email):
    results_dir = os.path.join(root, "results")
    repo = Repo(results_dir)
    repo.git.add(A=True)
    contents = repo.git.diff(cached=True)

    if contents:
        print contents
        if notification_email is not None:
            # email diffs
            print("TODO: email to " + notification_email)
        repo.index.commit(message)
    else:
        print("No changes")
    return
