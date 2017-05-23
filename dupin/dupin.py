import argparse
import os

from scanner import scan_repo, scan_repo_list
from organisation import update_organisation_repos


parser = argparse.ArgumentParser(description="Searches an organisation's repositories for Git secrets")
parser.add_argument("--root", help="Set the root directory for Dupin, defaults to CWD")
subparsers = parser.add_subparsers(title="Available commands", dest="subcommand")

update_repos_parser = subparsers.add_parser("update-repos", help="Lookup all the repositories for a Github organisation and update the local list",
                                      epilog="Example: dupin update-repos guardian abcdef12345")
update_repos_parser.add_argument("org", help="The name of the organisation to search")
update_repos_parser.add_argument("token", help="Access token for Github's API, this is used to discover the repositories")
update_repos_parser.add_argument("--file", help="write the list of repository URLs to this file (defaults to ROOT/repository-urls)",
                                 required=False)

scan_repo_parser = subparsers.add_parser("scan-repo", help="Look for secrets within a repository",
                                         epilog="Example: dupin scan https://github.com/guardian/dupin.git")
scan_repo_parser.add_argument("location", help="Location of the repository to check, can be local or remote")

scan_repos_parser = subparsers.add_parser("scan-repo-list", help="Search through a list of repositories, scanning each in turn",
                                          epilog="Example: dupin search my-repos.txt")
scan_repos_parser.add_argument("file", help="File containing a list of Git repositories to scan (as produced by `lookup`)")


def main():
    opts = parser.parse_args()
    if opts.root:
        root = opts.root
    else:
        root = os.getcwd()

    if "update-repos" == opts.subcommand:
        if opts.file:
            filename = opts.file
        else:
            filename = os.path.join(root, "repository-urls")
        update_organisation_repos(opts.org, opts.token, filename)
    elif "scan-repo" == opts.subcommand:
        scan_repo(opts.location, root)
    elif "scan-repo-list" == opts.subcommand:
        scan_repo_list(opts.file)
    return

if __name__ == "__main__":
    main()
