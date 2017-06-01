import os
import sys

from github import Github

from utils import printerr


def update_organisation_repos(organisation, token, filename):
    """Searches a Github organisation for repositories that can be
    cloned, writes discovered repo URLs to a local file."""
    github_client = Github(token)
    org = github_client.get_organization(organisation)

    printerr("Looking up {org} repositories (may take some time)".format(org=organisation))

    repos = org.get_repos("public")
    clone_urls = _clone_urls(repos)
    with open(filename, "w") as f:
        _write_repo_list(clone_urls, f)
        printerr("Wrote list of repositories to {location}".format(location=filename))
    return


def _clone_urls(repositories):
    return [ repo.clone_url for repo in repositories ]

def _write_repo_list(clone_urls, f):
    f.write("\n".join(clone_urls))
    return
