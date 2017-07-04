import argparse
import datetime
import os
import sys
import traceback
from textwrap import dedent

from scanner import scan_repo, scan_repo_list
from organisation import update_organisation_repos
from emails import send_email_properly
from history import history
from setup import setup
from config import Config


parser = argparse.ArgumentParser(description="Searches an organisation's repositories for Git secrets")
parser.add_argument("--root", help="Set the root directory for Dupin (default: CWD)")
parser.add_argument("--config", help="Set location of config file (default ROOT/config)")
subparsers = parser.add_subparsers(title="Available commands", dest="subcommand")

update_repos_parser = subparsers.add_parser("update-repos", help="Lookup all the repositories for a Github organisation and update the local list",
                                      epilog="Example: dupin update-repos guardian abcdef12345")
update_repos_parser.add_argument("org", nargs='?', help="The name of the organisation to search (default: from config)")
update_repos_parser.add_argument("--token", help="Access token for Github's API (default: from config)")
update_repos_parser.add_argument("--file", help="write the list of repository URLs to this file (default: ROOT/repository-urls)")
update_repos_parser.add_argument("--include-forks", action="store_true",
                                 help="By default Dupin excludes repositories that are 'forks', this flag changes that setting")
update_repos_parser.add_argument("--repo-exclusions", nargs='+',
                                 help="Exclude matching repos from the resulting list (useful for very large repos that cannot be scanned)")

scan_repo_parser = subparsers.add_parser("scan-repo", help="Look for secrets within a repository",
                                         epilog="Example: dupin scan https://github.com/guardian/dupin.git")
scan_repo_parser.add_argument("repo-url", help="URL of the repository to check")

scan_repo_list_parser = subparsers.add_parser("scan-repo-list", help="Search through a list of repositories, scanning each in turn",
                                              epilog="Example: dupin search my-repos.txt")
scan_repo_list_parser.add_argument("--repo-urls-file", help="File containing a list of Git repositories to scan (default: ROOT/repository-urls)")

history_parser = subparsers.add_parser("history", help="Show changes in discovered secrets for managed repositories",
                                       description="Dupin creates a Git repository to house scan results,\nthis command controls that repo.\nIt can also send email notifications to a configured email address.",
                                       epilog="Example: dupin history --notify")
history_parser.add_argument("--message", help="Commit message")
history_parser.add_argument("--notify", action="store_true", help="Send notifications of changes (reads email settings from config)")

setup_parser = subparsers.add_parser("setup", help="Setup a Dupin root directory",
                                     description="creates directory structure and initialises git repo for Dupin")

auto_parser = subparsers.add_parser("auto-scan-all", help="Scan all known repositories",
                                    description="Re-scan all known repositories (takes no other arguments but uses the provided root/config")
auto_parser.add_argument("--notify", action="store_true", help="Send notifications of changes (reads email settings from config)")


def main():
    try:
        opts = parser.parse_args()

        # shared settings
        if opts.root:
            root = opts.root
        else:
            root = os.getcwd()

        if opts.config:
            config = Config(opts.config)
        else:
            default_config = os.path.join(root, "config")
            if os.path.isfile(default_config):
                config = Config(default_config)
            else:
                config = Config()

        # subcommands
        if "setup" == opts.subcommand:
            setup(root)
        elif "update-repos" == opts.subcommand:
            org = opts.org or config.organisation_name
            repo_exclusions = opts.repo_exclusions or config.repo_exclusions
            if org is None:
                update_repos_parser.print_help()
                sys.exit(1)
            token = opts.token or config.github_token
            include_forks = opts.include_forks or config.include_forks or False
            if opts.file is None:
                filename = os.path.join(root, "repository-urls")
            else:
                filename = opts.file

            update_organisation_repos(org, token, filename, repo_exclusions, include_forks)
        elif "scan-repo" == opts.subcommand:
            repo_location = opts.location
            scan_repo(repo_location, root)
        elif "scan-repo-list" == opts.subcommand:
            if opts.file is None:
                repo_urls_filename = os.path.join(root, "repository-urls")
            else:
                repo_urls_filename = opts.file

            scan_repo_list(repo_urls_filename, root)
        elif "history" == opts.subcommand:
            history_message = opts.message or "Dupin search results"

            history(root, history_message, opts.notify, config)
        elif "auto-scan-all" == opts.subcommand:
            repo_urls_filename = os.path.join(root, "repository-urls")

            scan_repo_list(repo_urls_filename, root)
            history(root, "Dupin search results", opts.notify, config)
    except:
        if config.smtp_configured():
            stacktrace = traceback.format_exc().splitlines()
            message = dedent("""\
                Dupin failed during execution of {operation}
                
                Failed at: {timestamp}
                Exception details:
                {stacktrace}""").format(
                    operation=opts.subcommand,
                    stacktrace="\n".join(stacktrace),
                    timestamp=datetime.datetime.now().isoformat()
                )
            send_email_properly(message, config.notification_email, config.smtp_from, config.smtp_host, config.smtp_username, config.smtp_password)
        traceback.print_exc(file=sys.stderr)
    return

if __name__ == "__main__":
    main()
