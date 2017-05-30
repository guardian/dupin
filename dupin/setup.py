from __future__ import print_function

import os
from git import Repo

from utils import printerr


def setup(root):
    _create_skeleton(root)
    _initialise_history_repo(os.path.join(root, "results"))
    printerr("Dupin skeleton created at {location}".format(location=root))
    return


def _create_skeleton(root):
    os.makedirs(os.path.join(root, "repositories"))
    os.makedirs(os.path.join(root, "results"))
    with open(os.path.join(root, "repository-urls"), "w") as f:
        # touch file!
        pass
    return

def _initialise_history_repo(repo_path):
    repo = Repo.init(repo_path)
    with open(os.path.join(repo_path, "README.md"), "w") as readme:
        print(_README(), file=readme)
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")
    return

def _README():
    return """# Dupin results

This repository contains the history of Dupin's scans.
"""
