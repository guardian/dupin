from scan import scan_repo


def search_repo_list(filename):
    """Looks in the provided file and scans every repo found. Assumes the
file contains a list of repository URLs, with one on each line.
    """
    with open(filename, "r") as f:
        for repo_url in f:
            scan_repo(repo_url)
    return
