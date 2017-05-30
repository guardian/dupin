import os

from git import Repo

from utils import printerr


def history(root, message, notification_email):
    results_dir = os.path.join(root, "results")
    repo = Repo(results_dir)
    repo.git.add(A=True)
    contents = repo.git.diff(cached=True)

    if contents:
        if notification_email is not None:
            # email diffs
            print("TODO: email to " + notification_email)
        printerr("Changes to secrets detected")
        printerr("Comitting log to repo at {location}".format(location=results_dir))
        repo.index.commit(message)
    else:
        printerr("No new secrets found")
    return
