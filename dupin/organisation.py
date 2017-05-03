import sys

from github import Github


def _clone_urls(repositories):
    return [ repo.clone_url for repo in repositories ]

def _write_repo_list(clone_urls, f):
    f.write("\n".join(clone_urls))
    return


def lookup_organisation_repos(organisation, token, filename):
    """Searches a Github organisation for repositories that can be
    cloned, writes discovered repo URLs to a local file."""
    github_client = Github(token)
    org = github_client.get_organization(organisation)

    repos = org.get_repos()
    clone_urls = _clone_urls(repos)
    if filename is None:
        _write_repo_list(clone_urls, sys.stdout)
    else:
        with open(filename, "w") as f:
            _write_repo_list(clone_urls, f)

    return
