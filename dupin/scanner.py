import os
import truffleHog
from git import Repo
from urlparse import urlparse


def scan_repo(repo_url, root):
    repos_root = os.path.join(root, "repositories")
    results_file_path = os.path.join(repos_root, "results", _repo_name(repo_url))

    repo = _checkout_if_not_present(repo_url, repos_root)
    _find_secrets(repo, results_file_path)
    return

def scan_repo_list(filename):
    """Looks in the provided file and scans every repo found. Assumes the
file contains a list of repository URLs, with one on each line.
    """
    with open(filename, "r") as f:
        for repo_url in f:
            scan_repo(repo_url)
    return


def _checkout_if_not_present(repo_url, repos_root):
    """Returns the existing repository if it exists,
    otherwises puts a fresh clone in the right place
    """
    repo_name = _repo_name(repo_url)
    local_repo_path = os.path.join(repos_root, repo_name)
    if os.path.isdir(local_repo_path):
        return Repo(local_repo_path)
    else:
        return Repo.clone_from(repo_url, local_repo_path)

def _find_secrets(repo, output_file_path):
    """Uses trufflehog to search the repository for secrets and
    writes the log of what it finds to `output_file_path`.
    """
    with open(output_file_path, "w") as f:
        utf8_output = codecs.getwriter('utf8')
        utf8_f = utf8_output(f)
        return truffleHog.find_strings(repo, output_file=utf8_f)

def _repo_name(repo_url):
    return os.path.basename(urlparse(repo_url).path)
