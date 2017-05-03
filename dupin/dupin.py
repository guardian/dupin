import sys
import argparse

from organisation import lookup_organisation_repos
from scan import scan_repo
from search import search_repo_list


parser = argparse.ArgumentParser(description="Searches an organisation's repositories for Git secrets")
subparsers = parser.add_subparsers(title="Available commands", dest="subcommand")

lookup_parser = subparsers.add_parser("lookup", help="Lookup all the repositories for a Github organisation",
                                      epilog="Example: dupin lookup guardian abcdef12345")
lookup_parser.add_argument("org", help="The name of the organisation to search")
lookup_parser.add_argument("token", help="Access token for Github's API, this is used to discover the repositories")
lookup_parser.add_argument("--file", help="write the list of repository URLs to this file",
                           required=False, default=None)

scan_parser = subparsers.add_parser('scan', help="Look for secrets within a repository",
                                    epilog="Example: dupin scan https://github.com/guardian/dupin.git")
scan_parser.add_argument("location", help="Location of the repository to check, can be local or remote")

search_parser = subparsers.add_parser("search", help="Search through a list of repositories, sanning each in turn",
                                      epilog="Example: dupin search my-repos.txt")
search_parser.add_argument("file", help="File containing a list of Git repositories to scan (as produced by `lookup`)")


def main():
    opts = parser.parse_args()
    if "lookup" == opts.subcommand:
        repos = lookup_organisation_repos(opts.org, opts.token, opts.file)
    elif "scan" == opts.subcommand:
        scan_repo(opts.location)
    elif "search" == opts.subcommand:
        search_repo_list(opts.file)
    return

if __name__ == "__main__":
    main()
