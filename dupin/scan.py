import truffleHog


def scan_repo(repo_url):
    """Uses truffleHog to look through a repo's entire history. Prints
    what it finds to stdout.
    """
    truffleHog.find_strings(repo_url)
    return
